import asyncio
import sys
import threading
import functools
from typing import List, Any, Awaitable, TypeVar, Optional, Coroutine, Callable
from concurrent.futures import ThreadPoolExecutor

T = TypeVar('T')

class AltogetherContextManager:
    """Context manager for running async operations in parallel.
    
    Example usage:
    ```python
    with altogether:
        for x in range(5):
            altogether.add(do(x))  # These will run in parallel
        
        results = await altogether.all()  # Get all results
    ```
    """
    
    def __init__(self):
        self.tasks: List[asyncio.Task] = []
        self.active = False
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread_local = threading.local()
        self._thread_pool = ThreadPoolExecutor(max_workers=20)
        
    def __enter__(self):
        self.active = True
        self.tasks = []
        
        # Try to get an existing event loop or create a new one
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
        # Store the original event loop in thread-local storage
        self._thread_local.original_loop = self.loop
            
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.active = False
        
        if self.tasks:
            # Wait for all tasks to complete
            future = asyncio.gather(*self.tasks)
            
            if self._is_in_async_context():
                # We're already in an async context, just gather the tasks
                # but don't wait - the caller's event loop will handle that
                pass
            else:
                # We're in a sync context, run the loop until all tasks complete
                results = self.loop.run_until_complete(future)
                self._last_results = results
                
        # Clear tasks for next use
        self.tasks = []
    
    def _is_in_async_context(self) -> bool:
        """Check if we're currently in an async context."""
        try:
            # If this doesn't raise an exception, we're in an async context
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False
    
    def add(self, func: Callable, *args, **kwargs) -> asyncio.Task:
        """Add a blocking function to be executed in parallel.
        
        This should be called inside a 'with altogether:' block.
        """
        if not self.active:
            raise RuntimeError("Cannot add blocking function outside of 'with altogether' context")
        
        # Create a coroutine that runs the blocking function in a thread pool
        coro = self.to_async(func, *args, **kwargs)
        
        # Add the coroutine as a task
        return self.add_async(coro)
    
    def add_async(self, coro: Coroutine) -> asyncio.Task:
        """Add a coroutine to be executed in parallel.
        
        This should be called inside a 'with altogether:' block.
        """
        if not self.active:
            raise RuntimeError("Cannot add coroutine outside of 'with altogether' context")
        
        # Create a task for this coroutine
        task = asyncio.ensure_future(coro, loop=self.loop)
        self.tasks.append(task)
        return task
    
    async def to_async(self, func, *args, **kwargs):
        """Convert a blocking function to an awaitable coroutine.
        
        This runs the function in a thread pool and returns the result.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self._thread_pool, 
            functools.partial(func, *args, **kwargs)
        )
        
    async def all(self, tasks=None):
        """Wait for all tasks and return their results.
        
        If tasks is None, waits for all tasks added to the context.
        """
        if tasks is None:
            tasks = self.tasks
            
        return await asyncio.gather(*tasks)
        
    def all_sync(self, tasks=None):
        """Synchronous version of all() for use in non-async contexts.
        
        Returns the results of tasks when run in a synchronous context.
        """
        if not hasattr(self, '_last_results'):
            raise RuntimeError("No results available. Make sure to call this after the context has exited.")
        return self._last_results
    
    async def __aenter__(self):
        """Support for async with."""
        return self.__enter__()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Support for async with."""
        return self.__exit__(exc_type, exc_val, exc_tb)


# Create the singleton instance
altogether = AltogetherContextManager()
