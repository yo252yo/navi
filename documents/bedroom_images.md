Sure! Here's how to add your bedroom/computer images:
For the bedroom background:

body {
    background-image: url('path/to/bedroom.jpg');
    background-size: cover;
    background-position: center;
}

For the computer/monitor:
You have two main options:

Replace the monitor frame - Add a background image to .monitor-frame:

.monitor-frame {
    background-image: url('path/to/computer.png');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
}

This works if your computer image includes the whole desk setup.

Layered approach (more flexible) - Remove the gradient from .monitor-frame and position your computer image behind it, or add it as a ::before pseudo-element.

Pro tip: Make sure your computer image has a transparent "screen area" in the middle, or crop it to just show the bezel/frame around where the iframe sits. That way the iframe shows through as the actual screen content.
The current gray frame gives you the exact dimensions and position where your monitor bezel should be!