"""
Metro Ticket Purchasing System
A simple, clean command-line application for purchasing metro tickets.
"""

import csv
import os
import uuid
from collections import deque
from typing import List, Dict, Tuple, Optional

# Optional visualization imports
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Note: Install networkx and matplotlib for metro map visualization")
    print("Run: pip install networkx matplotlib\n")


class Station:
    """Represents a metro station with its connections and lines."""
    
    def __init__(self, name: str, lines: List[str], connections: Dict[str, str]):
        """
        Initialize a Station.
        
        Args:
            name: Station name
            lines: List of metro lines this station is on
            connections: Dict mapping neighbor station names to the connecting line
        """
        self.name = name
        self.lines = lines  # List of lines this station is on
        self.connections = connections  # {neighbor_name: line_name}
    
    def __str__(self):
        return f"{self.name} (Lines: {', '.join(self.lines)})"
    
    def is_interchange(self) -> bool:
        """Check if this station is an interchange (on multiple lines)."""
        return len(self.lines) > 1


class Line:
    """Represents a metro line."""
    
    def __init__(self, name: str, color: str):
        """
        Initialize a Line.
        
        Args:
            name: Line name (e.g., "Red", "Blue")
            color: Display color for visualization
        """
        self.name = name
        self.color = color
        self.stations = []  # List of station names on this line
    
    def __str__(self):
        return f"{self.name} Line"


class Ticket:
    """Represents a purchased metro ticket."""
    
    def __init__(self, ticket_id: str, user_name: str, origin: str, 
                 destination: str, price: float, path: List[str], instructions: List[str]):
        """
        Initialize a Ticket.
        
        Args:
            ticket_id: Unique ticket identifier
            user_name: Name of the user who purchased the ticket
            origin: Starting station
            destination: Ending station
            price: Ticket price
            path: List of stations in the journey
            instructions: List of travel instructions
        """
        self.ticket_id = ticket_id
        self.user_name = user_name
        self.origin = origin
        self.destination = destination
        self.price = price
        self.path = path
        self.instructions = instructions
    
    def __str__(self):
        return (f"Ticket ID: {self.ticket_id}\n"
                f"From: {self.origin} → To: {self.destination}\n"
                f"Price: Rs. {self.price}")


class User:
    """Represents a user of the metro system."""
    
    def __init__(self, name: str):
        """
        Initialize a User.
        
        Args:
            name: User's name
        """
        self.name = name
        self.tickets = []  # List of ticket IDs
    
    def __str__(self):
        return f"User: {self.name}"


class MetroSystem:
    """Main class managing the entire metro system."""
    
    # Pricing constants
    BASE_FARE = 10  # Base fare in Rs.
    PER_STATION_FARE = 5  # Additional fare per station in Rs.
    
    def __init__(self):
        """Initialize the metro system and load data from CSV files."""
        self.stations: Dict[str, Station] = {}
        self.lines: Dict[str, Line] = {}
        self.tickets: List[Ticket] = []
        self.users: Dict[str, User] = {}
        
        # Load data from CSV files
        self.load_stations()
        self.load_users()
        self.load_tickets()

    def load_stations(self):
        """Load stations from CSV file."""
        if not os.path.exists('stations.csv'):
            print("Warning: stations.csv not found. Please run reset_csvs.py to initialize.")
            return
        
        with open('stations.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                lines = row['lines'].split(';') if row['lines'] else []
                
                # Parse connections
                connections = {}
                if row['neighbours']:
                    for connection in row['neighbours'].split(';'):
                        if ':' in connection:
                            neighbor, line = connection.split(':')
                            connections[neighbor] = line
                
                # Create station
                station = Station(name, lines, connections)
                self.stations[name] = station
                
                # Update lines
                for line_name in lines:
                    if line_name not in self.lines:
                        # Default colors for common line names
                        colors = {'Red': 'red', 'Blue': 'blue', 'Green': 'green', 
                                 'Yellow': 'yellow', 'Purple': 'purple', 'Orange': 'orange'}
                        color = colors.get(line_name, 'gray')
                        self.lines[line_name] = Line(line_name, color)
                    self.lines[line_name].stations.append(name)
    
    def load_users(self):
        """Load users from CSV file."""
        if not os.path.exists('users.csv'):
            return
        
        with open('users.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(row['user_name'])
                self.users[user.name] = user

    def load_tickets(self):
        """Load tickets from CSV file."""
        if not os.path.exists('tickets.csv'):
            return
        
        with open('tickets.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                path = row['path'].split(';') if row.get('path') else []
                instructions = row['instructions'].split('|') if row.get('instructions') else []
                
                ticket = Ticket(
                    ticket_id=row['ticket_id'],
                    user_name=row['user_name'],
                    origin=row['origin'],
                    destination=row['destination'],
                    price=float(row['price']),
                    path=path,
                    instructions=instructions
                )
                self.tickets.append(ticket)

                # Add ticket to user
                if ticket.user_name in self.users:
                    self.users[ticket.user_name].tickets.append(ticket.ticket_id)
    
    def save_user(self, user: User):
        """Save a new user to CSV file."""
        fieldnames = ['user_name']
        write_header = not os.path.exists('users.csv')
        
        with open('users.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow({'user_name': user.name})
    
    def save_ticket(self, ticket: Ticket):
        """Save a new ticket to CSV file."""
        fieldnames = ['ticket_id', 'user_name', 'origin', 'destination', 
                     'price', 'path', 'instructions']
        write_header = not os.path.exists('tickets.csv')
        
        with open('tickets.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow({
                'ticket_id': ticket.ticket_id,
                'user_name': ticket.user_name,
                'origin': ticket.origin,
                'destination': ticket.destination,
                'price': ticket.price,
                'path': ';'.join(ticket.path),
                'instructions': '|'.join(ticket.instructions)
            })
    
    def display_all_stations(self):
        """Display all available metro stations."""
        if not self.stations:
            print("No stations available. Please initialize the system.")
            return
        
        print("\n" + "="*60)
        print("AVAILABLE METRO STATIONS")
        print("="*60)
        
        # Group stations by line for better display
        for line_name, line in sorted(self.lines.items()):
            print(f"\n{line_name} Line:")
            print("-" * 30)
            for station_name in line.stations:
                station = self.stations[station_name]
                interchange = " (Interchange)" if station.is_interchange() else ""
                print(f"  • {station.name}{interchange}")
    
    def find_shortest_path(self, origin: str, destination: str) -> Optional[List[str]]:
        """
        Find the shortest path between two stations using BFS.
        
        Args:
            origin: Starting station name
            destination: Ending station name
            
        Returns:
            List of station names representing the path, or None if no path exists
        """
        if origin not in self.stations or destination not in self.stations:
            return None
        
        if origin == destination:
            return [origin]
        
        # BFS to find shortest path
        queue = deque([[origin]])
        visited = set()
        
        while queue:
            path = queue.popleft()
            current_station = path[-1]
            
            if current_station == destination:
                return path
            
            if current_station not in visited:
                visited.add(current_station)
                
                # Add all neighbors to queue
                for neighbor in self.stations[current_station].connections:
                    if neighbor not in visited:
                        new_path = path + [neighbor]
                    queue.append(new_path)
        
        return None
    
    def generate_travel_instructions(self, path: List[str]) -> List[str]:
        """
        Generate detailed travel instructions for a path.
        
        Args:
            path: List of station names
            
        Returns:
            List of instruction strings
        """
        if not path or len(path) < 2:
            return []

        instructions = []
        current_line = None
        boarding_station = path[0]
        
        for i in range(len(path) - 1):
            from_station = self.stations[path[i]]
            to_station_name = path[i + 1]
            
            # Get the line connecting these stations
            line = from_station.connections.get(to_station_name)
            
            if line != current_line:
                if current_line is not None:
                    # Line change needed
                    instructions.append(f"Get off at {path[i]}")
                    instructions.append(f"Change to {line} Line at {path[i]}")
                    boarding_station = path[i]
                else:
                    # First boarding
                    instructions.append(f"Board {line} Line at {path[0]}")
                current_line = line
        
        # Final instruction
        instructions.append(f"Travel on {current_line} Line from {boarding_station} to {path[-1]}")
        instructions.append(f"Get off at {path[-1]} (Destination)")
        
        return instructions
    
    def calculate_fare(self, path: List[str]) -> float:
        """
        Calculate the fare based on the number of stations.
        
        Args:
            path: List of station names
            
        Returns:
            Fare amount in Rs.
        """
        if not path or len(path) < 2:
            return 0
        
        # Base fare + additional fare per station crossed
        stations_crossed = len(path) - 1
        fare = self.BASE_FARE + (stations_crossed * self.PER_STATION_FARE)
        return fare
    
    def purchase_ticket(self, user_name: str, origin: str, destination: str) -> Optional[Ticket]:
        """
        Purchase a ticket for a journey.
        
        Args:
            user_name: Name of the user
            origin: Starting station
            destination: Ending station
            
        Returns:
            The purchased ticket or None if purchase failed
        """
        # Validate stations
        if origin not in self.stations:
            print(f"Error: Origin station '{origin}' not found.")
            return None
        
        if destination not in self.stations:
            print(f"Error: Destination station '{destination}' not found.")
            return None
        
        # Find shortest path
        path = self.find_shortest_path(origin, destination)
        if not path:
            print(f"Error: No route available from {origin} to {destination}.")
            return None
        
        # Create or get user
        if user_name not in self.users:
            user = User(user_name)
            self.users[user_name] = user
            self.save_user(user)
        
        # Generate instructions and calculate fare
        instructions = self.generate_travel_instructions(path)
        fare = self.calculate_fare(path)
        
        # Create ticket
        ticket_id = str(uuid.uuid4())
        ticket = Ticket(
            ticket_id=ticket_id,
            user_name=user_name,
            origin=origin,
            destination=destination,
            price=fare,
            path=path,
            instructions=instructions
        )
        
        # Save ticket
        self.tickets.append(ticket)
        self.users[user_name].tickets.append(ticket_id)
        self.save_ticket(ticket)
        
        return ticket
    
    def view_user_tickets(self, user_name: str):
        """Display all tickets for a user."""
        if user_name not in self.users:
            print(f"No tickets found for user: {user_name}")
            return
        
        user_tickets = [t for t in self.tickets if t.user_name == user_name]
        
        if not user_tickets:
            print(f"No tickets found for user: {user_name}")
            return
        
        print(f"\n" + "="*60)
        print(f"TICKETS FOR: {user_name}")
        print("="*60)
        
        for i, ticket in enumerate(user_tickets, 1):
            print(f"\n[Ticket {i}]")
            print("-" * 40)
            print(f"Ticket ID: {ticket.ticket_id}")
            print(f"Journey: {ticket.origin} → {ticket.destination}")
            print(f"Price: Rs. {ticket.price}")
            print(f"Route: {' → '.join(ticket.path)}")
            print("\nTravel Instructions:")
            for instruction in ticket.instructions:
                print(f"  • {instruction}")
    
    def visualize_metro_map(self):
        """Create a visual representation of the metro network."""
        if not VISUALIZATION_AVAILABLE:
            print("\nVisualization not available. Please install required packages:")
            print("pip install networkx matplotlib")
            return
        
        if not self.stations:
            print("No stations to visualize.")
            return
        
        # Create graph
        G = nx.Graph()
        
        # Add edges with colors
        edge_colors = []
        edge_labels = {}
        
        for station in self.stations.values():
            for neighbor, line in station.connections.items():
                if G.has_edge(station.name, neighbor):
                    continue
                
                G.add_edge(station.name, neighbor)
                line_obj = self.lines.get(line)
                color = line_obj.color if line_obj else 'gray'
                edge_colors.append(color)
                edge_labels[(station.name, neighbor)] = line
        
        # Create layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Draw the graph
        plt.figure(figsize=(12, 8))
        plt.title("Metro Network Map", fontsize=16, fontweight='bold')
        
        # Draw nodes (stations)
        interchange_stations = [s.name for s in self.stations.values() if s.is_interchange()]
        regular_stations = [s.name for s in self.stations.values() if not s.is_interchange()]
        
        # Draw regular stations
        nx.draw_networkx_nodes(G, pos, nodelist=regular_stations, 
                              node_color='lightblue', node_size=1000, label='Station')
        
        # Draw interchange stations
        nx.draw_networkx_nodes(G, pos, nodelist=interchange_stations,
                              node_color='yellow', node_size=1500, 
                              node_shape='s', label='Interchange')
        
        # Draw edges (connections)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=3)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                     font_size=8, font_color='darkred')
        
        # Add legend
        plt.legend(loc='upper left')
        
        # Remove axes
        plt.axis('off')
        plt.tight_layout()
        plt.show()


def main():
    """Main function to run the metro ticket system."""
    print("\n" + "="*60)
    print(" "*15 + "METRO TICKET SYSTEM")
    print("="*60)
    
    # Initialize system
    metro = MetroSystem()
    
    while True:
        print("\n" + "-"*40)
        print("MAIN MENU")
        print("-"*40)
        print("1. Show all stations")
        print("2. Purchase ticket")
        print("3. View my tickets")
        if VISUALIZATION_AVAILABLE:
            print("4. Visualize metro map")
        print("0. Exit")
        print("-"*40)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            metro.display_all_stations()
        
        elif choice == '2':
            print("\n" + "="*40)
            print("PURCHASE TICKET")
            print("="*40)
            
            user_name = input("Enter your name: ").strip()
            if not user_name:
                print("Error: Name cannot be empty.")
                continue
            
            print("\nAvailable stations:")
            station_names = sorted(metro.stations.keys())
            for name in station_names:
                print(f"  • {name}")
            
            origin = input("\nEnter origin station: ").strip()
            destination = input("Enter destination station: ").strip()
            
            ticket = metro.purchase_ticket(user_name, origin, destination)
            
            if ticket:
                print("\n" + "="*50)
                print("TICKET PURCHASED SUCCESSFULLY!")
                print("="*50)
                print(ticket)
                print(f"\nRoute: {' → '.join(ticket.path)}")
                print(f"Stations to cross: {len(ticket.path) - 1}")
                print("\nTravel Instructions:")
                for instruction in ticket.instructions:
                    print(f"  • {instruction}")
                print("-"*50)
        
        elif choice == '3':
            user_name = input("Enter your name: ").strip()
            if user_name:
                metro.view_user_tickets(user_name)
            else:
                print("Error: Name cannot be empty.")
        
        elif choice == '4' and VISUALIZATION_AVAILABLE:
            print("\nGenerating metro map visualization...")
            metro.visualize_metro_map()
        
        elif choice == '0':
            print("\nThank you for using Metro Ticket System!")
            print("Have a safe journey!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()