
# 📦 Packet Transmission Protocol

This project simulates a basic packet-based communication system between two endpoints – a **Sender** and a **Receiver** – using a simplified, custom transmission protocol.

## 👨‍💻 Project Structure

The core of the project includes the following classes:

- **`Packet`** – Represents a data packet containing source/destination addresses, a sequence number, ACK flag, and payload data.
- **`Communicator`** – A base class for both sender and receiver, holding shared attributes like address and sequence handling.
- **`Sender`** – Splits messages into packets, assigns sequence numbers, and sends them.
- **`Receiver`** – Receives packets, stores them, and returns acknowledgments (ACKs).

## 📌 Key Features

- Splits long messages into fixed-size packets (default: 3 characters).
- Tracks each packet using sequence numbers.
- Handles acknowledgment (ACK) packets for confirming successful delivery.
- Simulates packet sending/receiving and prints status updates to the console.

## 🧪 Example Usage

```python
sender = Sender(address="192.168.1.1", num_letters_in_packet=3)
receiver = Receiver(address="192.168.1.2")

packets = sender.prepare_packets("HelloWorld", destination_address=receiver.get_address())

for packet in packets:
    sent_packet = sender.send_packet(packet)
    receiver.receive_packet(sent_packet)
    ack = Packet(receiver.get_address(), sender.get_address(), packet.get_sequence_number(), is_ack=True)
    sender.receive_ack(ack)
```

## 📁 Files

- `PacketTransmissionProtocolProject.py` – The main Python file containing all logic and class definitions.

## 🚀 Future Enhancements

- Introduce random transmission errors and implement retransmission logic.
- Add support for more advanced protocols like Go-Back-N or Selective Repeat.
- Create a simple command-line or graphical interface for running simulations.
- Export transmission logs to file.
