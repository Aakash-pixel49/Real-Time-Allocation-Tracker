import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Setup the figure
fig, ax = plt.subplots()
x_data, y_data = [], []

# Global variable to track memory
current_memory = 0

def animate(i):
    global current_memory
    
    # If the log file doesn't exist yet, just return
    if not os.path.exists("memory.log"):
        return
    
    try:
        with open("memory.log", "r") as f:
            lines = f.readlines()
            
        # Re-calculate memory from scratch to handle updates
        # (In a real app, we would optimize this to read only new lines)
        temp_mem = 0
        y_vals = []
        
        for line in lines:
            parts = line.split()
            if len(parts) < 2: continue
            
            action = parts[0]
            size = int(parts[1])
            
            if action == "ALLOC":
                temp_mem += size
            elif action == "FREE":
                # When freeing, we decrease usage. 
                # (Logic simplified for visualization demo)
                if temp_mem > 0:
                    temp_mem -= 1024 # illustrative decrease
            
            y_vals.append(temp_mem)

        # Update the graph
        ax.clear()
        ax.plot(y_vals, label='Heap Usage (Bytes)', color='blue')
        ax.set_title('Real-Time Memory Allocation Tracker')
        ax.set_ylabel('Bytes Allocated')
        ax.set_xlabel('Time (Events)')
        ax.legend(loc='upper left')
        ax.grid(True)
        
    except Exception as e:
        print(f"Error reading log: {e}")

# Refresh the graph every 1000 milliseconds (1 second)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()