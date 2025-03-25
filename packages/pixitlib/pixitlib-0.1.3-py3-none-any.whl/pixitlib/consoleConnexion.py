import socket
import sys

class GameConnexion:
    def __init__(self, host="127.0.0.1", console_port=58591, processing_port=15426, player_count=1):
        self.host = host
        self.console_port = console_port
        self.processing_port = processing_port
        self.player_count = player_count

        self.console_socket = None
        self.processing_socket = None
        self.running = True

    def connect(self, game=None):
        """Établit les connexions à la console et à Processing"""
        # Connexion à la console
        self.console_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.console_socket.connect((self.host, self.console_port))

        # Connexion à Processing
        self.processing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.processing_socket.connect((self.host, self.processing_port))

    def send_frame(self, frame=None):
        """Envoie une trame à Processing"""
        if frame is not None:
            self.processing_socket.sendall(frame.encode())

    def listen_for_commands(self):
        """Écoute les commandes de la console et les traite"""
        while self.running:
            try:
                command = self.console_socket.recv(1024).decode().strip()
                if not command:
                    continue
                
                if command == "KILL":
                    self.running = False
                    break
                
                # Renvoyer la commande au jeu (sera utilisé par le jeu)
                yield command
                
            except ConnectionResetError:
                print("Connexion à la console perdue.")
                self.running = False
            except Exception as e:
                print(f"Erreur: {e}")
                self.running = False

    def close(self):
        """Ferme les connexions"""
        if self.processing_socket:
            self.processing_socket.close()
        if self.console_socket:
            self.console_socket.close()
        sys.exit(0)