"""
Progress tracking utilities for interactive environments like Jupyter notebooks.

This module provides tools for displaying progress of long-running operations,
especially useful for deduplication tasks that involve many comparisons.
"""

import sys
import time
import psutil
from typing import Optional, Callable, Dict, Any, Union, List
from datetime import datetime, timedelta

# Detect environment (Jupyter or command line)
try:
    from IPython import get_ipython
    if get_ipython() is not None and 'IPython.core.interactiveshell' in str(type(get_ipython())):
        from IPython.display import display, clear_output
        from ipywidgets import HTML, HBox, VBox, IntProgress, Label, Layout, Box, Output
        JUPYTER_AVAILABLE = True
    else:
        JUPYTER_AVAILABLE = False
except ImportError:
    JUPYTER_AVAILABLE = False

class ProgressTracker:
    """
    Track progress of long-running operations with real-time visual feedback.
    
    This class provides a progress bar and statistics about ongoing operations,
    with different display modes for Jupyter notebooks and command line interfaces.
    """
    
    def __init__(
        self, 
        total: int,
        description: str = "Processing",
        update_interval: float = 0.5,
        memory_tracking: bool = True,
        eta_calculation: bool = True,
        jupyter_mode: Optional[bool] = None,
        width: str = '100%'
    ):
        """
        Initialize a progress tracker.
        
        Parameters
        ----------
        total : int
            Total number of operations to track
        description : str, default="Processing"
            Description of the operation being tracked
        update_interval : float, default=0.5
            Minimum time in seconds between display updates
        memory_tracking : bool, default=True
            Whether to track and display memory usage
        eta_calculation : bool, default=True
            Whether to calculate and display estimated time remaining
        jupyter_mode : Optional[bool], default=None
            Force Jupyter or command line mode; if None, auto-detect
        width : str, default='100%'
            Width of the progress display in Jupyter mode
        """
        self.total = total
        self.completed = 0
        self.description = description
        self.update_interval = update_interval
        self.memory_tracking = memory_tracking
        self.eta_calculation = eta_calculation
        self.width = width
        
        # Auto-detect or force Jupyter mode
        if jupyter_mode is None:
            self.jupyter_mode = JUPYTER_AVAILABLE
        else:
            self.jupyter_mode = jupyter_mode and JUPYTER_AVAILABLE
            
        # Initialize timing variables
        self.start_time = None
        self.last_update_time = 0
        self.last_display_time = 0
        self.last_memory_check = 0
        self.current_memory_usage = 0
        self.peak_memory_usage = 0
        self.speeds = []  # To keep track of recent speeds
        
        # Jupyter-specific components
        if self.jupyter_mode:
            self.progress_bar = IntProgress(
                value=0,
                min=0,
                max=total,
                description=description,
                bar_style='info',
                style={'bar_color': '#1a75ff'},
                layout=Layout(width=width)
            )
            self.status_label = Label(value="Starting...")
            self.eta_label = Label(value="")
            self.memory_label = Label(value="")
            self.output = Output()
            
            # Combine all elements into a vertical layout
            self.display_box = VBox([
                self.progress_bar,
                HBox([self.status_label, self.eta_label, self.memory_label])
            ])
            
            # Display the progress tracker
            display(self.display_box)
    
    def start(self) -> None:
        """Start the progress tracking."""
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_display_time = self.start_time
        self.completed = 0
        self.speeds = []
        
        # Initial memory check
        if self.memory_tracking:
            self._update_memory_usage()
    
    def update(self, increment: int = 1, force_display: bool = False) -> None:
        """
        Update progress tracker with completed items.
        
        Parameters
        ----------
        increment : int, default=1
            Number of items completed since last update
        force_display : bool, default=False
            Whether to force a display update regardless of update interval
        """
        if self.start_time is None:
            self.start()
            
        current_time = time.time()
        self.completed += increment
        
        # Calculate speed
        time_diff = current_time - self.last_update_time
        if time_diff > 0:
            # Add current speed to the speeds list (items per second)
            speed = increment / time_diff
            self.speeds.append(speed)
            # Keep only the 10 most recent speeds for better adaptability
            if len(self.speeds) > 10:
                self.speeds.pop(0)
            self.last_update_time = current_time
        
        # Update display if enough time has passed or forced
        if force_display or (current_time - self.last_display_time >= self.update_interval):
            self._update_display()
            self.last_display_time = current_time
    
    def finish(self) -> None:
        """Mark the progress tracking as complete."""
        self.completed = self.total
        self._update_display(final=True)
        
        if self.jupyter_mode:
            self.progress_bar.bar_style = 'success'
            self.status_label.value = f"Complete: {self.total}/{self.total} ({100:.1f}%)"
    
    def _update_memory_usage(self) -> None:
        """Update memory usage statistics."""
        if not self.memory_tracking:
            return
            
        current_time = time.time()
        # Only check memory every 2 seconds to reduce overhead
        if current_time - self.last_memory_check < 2:
            return
            
        process = psutil.Process()
        self.current_memory_usage = process.memory_info().rss / (1024 * 1024)  # MB
        self.peak_memory_usage = max(self.peak_memory_usage, self.current_memory_usage)
        self.last_memory_check = current_time
    
    def _calculate_eta(self) -> Optional[str]:
        """Calculate estimated time remaining."""
        if not self.eta_calculation or self.completed == 0:
            return None
            
        elapsed = time.time() - self.start_time
        
        # Use average speed of recent updates
        if self.speeds:
            avg_speed = sum(self.speeds) / len(self.speeds)
            remaining_items = self.total - self.completed
            
            if avg_speed > 0:
                eta_seconds = remaining_items / avg_speed
                eta = timedelta(seconds=int(eta_seconds))
                return str(eta)
        
        return None
    
    def _update_display(self, final: bool = False) -> None:
        """
        Update the progress display.
        
        Parameters
        ----------
        final : bool, default=False
            Whether this is the final update
        """
        # Update memory usage
        if self.memory_tracking:
            self._update_memory_usage()
        
        # Calculate metrics
        percent = (self.completed / self.total) * 100 if self.total > 0 else 0
        eta = self._calculate_eta()
        
        if self.jupyter_mode:
            # Update Jupyter components
            self.progress_bar.value = self.completed
            self.status_label.value = f"Progress: {self.completed:,}/{self.total:,} ({percent:.1f}%)"
            
            if eta:
                self.eta_label.value = f"ETA: {eta}"
            
            if self.memory_tracking:
                self.memory_label.value = f"Memory: {self.current_memory_usage:.1f} MB (peak: {self.peak_memory_usage:.1f} MB)"
        else:
            # Command line display
            bar_length = 50
            filled_length = int(bar_length * self.completed // self.total)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            status = f"\r{self.description}: [{bar}] {self.completed:,}/{self.total:,} ({percent:.1f}%)"
            
            if eta:
                status += f" ETA: {eta}"
                
            if self.memory_tracking:
                status += f" | Memory: {self.current_memory_usage:.1f} MB"
                
            # Print with carriage return for updating in-place
            if final:
                print(status)
            else:
                print(status, end='', flush=True)


class BlockProgressTracker(ProgressTracker):
    """
    Extended progress tracker for tracking progress across multiple blocks.
    
    This tracker handles deduplication scenarios where data is processed in blocks,
    showing both overall progress and current block progress.
    """
    
    def __init__(
        self,
        total_blocks: int,
        description: str = "Processing blocks",
        **kwargs
    ):
        """
        Initialize a block progress tracker.
        
        Parameters
        ----------
        total_blocks : int
            Total number of blocks to process
        description : str, default="Processing blocks"
            Description of the operation being tracked
        **kwargs : dict
            Additional arguments to pass to ProgressTracker
        """
        super().__init__(total=total_blocks, description=description, **kwargs)
        
        self.total_blocks = total_blocks
        self.current_block = 0
        self.block_progress = None
        
        # Add block-specific display for Jupyter
        if self.jupyter_mode:
            self.block_label = Label(value="")
            self.display_box.children = list(self.display_box.children) + [
                Label(value="Current block:"),
                self.block_label
            ]
    
    def start_block(self, block_id: int, block_size: int, description: Optional[str] = None) -> "ProgressTracker":
        """
        Start tracking a new block.
        
        Parameters
        ----------
        block_id : int
            ID of the block being processed
        block_size : int
            Size of the block (number of operations)
        description : Optional[str], default=None
            Description of the block; if None, uses "Block {block_id}/{total_blocks}"
            
        Returns
        -------
        ProgressTracker
            A tracker for the current block
        """
        self.current_block = block_id
        
        if description is None:
            description = f"Block {block_id}/{self.total_blocks}"
            
        # Update the block label in Jupyter mode
        if self.jupyter_mode:
            self.block_label.value = f"{description} - Size: {block_size:,} items"
        
        # Create a tracker for this block
        self.block_progress = ProgressTracker(
            total=block_size,
            description=description,
            update_interval=self.update_interval,
            memory_tracking=self.memory_tracking,
            eta_calculation=self.eta_calculation,
            jupyter_mode=self.jupyter_mode,
            width=self.width
        )
        self.block_progress.start()
        
        return self.block_progress
    
    def finish_block(self) -> None:
        """Mark the current block as complete."""
        if self.block_progress:
            self.block_progress.finish()
            
        # Update the main progress
        self.update(1, force_display=True)
        
        # Clean up
        self.block_progress = None


# Convenience function to create a tracker for deduplication tasks
def create_deduplication_tracker(
    total_comparisons: int,
    description: str = "Deduplication progress",
    **kwargs
) -> ProgressTracker:
    """
    Create a progress tracker specifically configured for deduplication tasks.
    
    Parameters
    ----------
    total_comparisons : int
        Total number of pairwise comparisons to make
    description : str, default="Deduplication progress"
        Description of the deduplication operation
    **kwargs : dict
        Additional parameters to pass to ProgressTracker
        
    Returns
    -------
    ProgressTracker
        A configured progress tracker
    """
    return ProgressTracker(
        total=total_comparisons,
        description=description,
        memory_tracking=True,
        eta_calculation=True,
        **kwargs
    )