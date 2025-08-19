class Packet:
    def __init__(self, source_address, destination_address, sequence_number,
               is_ack=False, data=None):
        """Initialize a Packet object."""
        self.__source_address = source_address
        self.__destination_address = destination_address
        self.__sequence_number = sequence_number
        self.__is_ack = is_ack
        self.__data = data
        pass

    def __repr__(self):
        """Return a string representation of the Packet object."""
        return (f"Packet(Source IP: {self.__source_address}, Dest IP: {self.__destination_address}, "
                f"#Seq: {self.__sequence_number}, Is ACK: {self.__is_ack}, Data: {self.__data})")

    def get_source_address(self):
        return self.__source_address
        pass

    def get_destination_address(self):
        return self.__destination_address
        pass

    def get_sequence_number(self):
        return self.__sequence_number
        pass

    def set_sequence_number(self, seq_num):
        self.__sequence_number = seq_num
        pass

    def get_is_ack(self):
        return self.__is_ack
        pass

    def get_data(self):
        return self.__data
        pass


class Communicator:
    """Initialize a Communicator object."""
    def __init__(self, address):
        self.__address = address
        self.__sequence_number = None
        pass

    def get_address(self):
        return self.__address
        pass

    def get_current_sequence_number(self):
        return self.__sequence_number
        pass

    def set_current_sequence_number(self, seq_num):
        self.__sequence_number = seq_num
        pass

    def send_packet(self, packet):
        print(f"Sender: Packet Seq Num: {self.__sequence_number} was sent")
        return packet
        pass

    def increment_current_seq_num(self):
        self.__sequence_number += 1
        pass


class Sender(Communicator):
    """Initialize a Sender object."""
    def __init__(self, address, num_letters_in_packet):
        super().__init__(address)
        self.__num_letters_in_packet = num_letters_in_packet
        self.__source_address = None
        pass

    def prepare_packets(self, message, destination_address):
        """Prepare packets from the message to be sent."""
        Packet_Size = 3
        packets = [message[i:i + Packet_Size] for i in range(0, len(message), Packet_Size)]
        packets = [packet.ljust(Packet_Size) for packet in packets]
        packet_objects = [Packet(self.__source_address, destination_address, i, False, packets[i]) for i in
                          range(len(packets))]
        return packet_objects
        pass

    def receive_ack(self, acknowledgment_packet):
        return acknowledgment_packet.get_is_ack()
        pass


class Receiver(Communicator):
    """Initialize a Receiver object."""
    def __init__(self, address):
        super().__init__(address)
        self.packets_received = []
        pass

    def receive_packet(self, packet):
        """Receive a packet and add it to the received packets list."""
        self.packets_received.append(packet)
        acknowledgment = Packet(source_address=self.get_address(),
                                destination_address=packet.get_source_address(),
                                sequence_number=packet.get_sequence_number(),
                                is_ack=True)
        print(f"Receiver: Received packet seq num: {acknowledgment.get_sequence_number()}")
        return acknowledgment
        pass

    def get_message_by_received_packets(self):
        """Get the message assembled from received packets."""
        message = "".join(packet.get_data() for packet in self.packets_received)
        return message
        pass


if __name__ == '__main__':
    source_address = "192.168.1.1"
    destination_address = "192.168.2.2"
    message = "what is up?"
    num_letters_in_packet = 3

    sender = Sender(source_address, num_letters_in_packet)
    receiver = Receiver(destination_address)

    packets = sender.prepare_packets(message, receiver.get_address())

    # setting current packet
    start_interval_index = packets[0].get_sequence_number()
    # setting current packet in the sender and receiver
    sender.set_current_sequence_number(start_interval_index)
    receiver.set_current_sequence_number(start_interval_index)

    # setting the last packet
    last_packet_sequence_num = packets[-1].get_sequence_number()
    receiver_current_packet = receiver.get_current_sequence_number()

    while receiver_current_packet <= last_packet_sequence_num:
        current_index = sender.get_current_sequence_number()
        packet = packets[current_index]
        packet = sender.send_packet(packet)

        ack = receiver.receive_packet(packet)

        result = sender.receive_ack(ack)

        if result == True:
            sender.increment_current_seq_num()
            receiver.increment_current_seq_num()

        receiver_current_packet = receiver.get_current_sequence_number()

    full_message = receiver.get_message_by_received_packets()
    print(f"Receiver message: {full_message}")