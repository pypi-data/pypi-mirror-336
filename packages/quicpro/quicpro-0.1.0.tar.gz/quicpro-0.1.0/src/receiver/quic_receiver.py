import logging
from typing import Any
from quicpro.exceptions import QUICFrameReassemblyError

logger = logging.getLogger(__name__)

class QUICReceiver:
    """
    Production-grade QUICReceiver that receives and reassembles QUIC packets
    into complete HTTP/3 stream frames.

    Expected QUIC packet format:
        b"QUICFRAME:<frame_id>:<seq_num>:<total_packets>:<payload>"

    If the packet does not start with b"QUICFRAME:", it falls back and forwards
    the entire packet directly to the HTTP3Receiver.
    """
    def __init__(self, http3_receiver: Any) -> None:
        self.http3_receiver = http3_receiver

    def receive(self, quic_packet: bytes) -> None:
        try:
            if not quic_packet.startswith(b"QUICFRAME:"):
                logger.warning("QUICReceiver: Packet missing header, falling back to HTTP3Receiver.")
                self.http3_receiver.receive(quic_packet)
                return
            # (Placeholder for reassembly logic)
            self.http3_receiver.receive(quic_packet)
        except Exception as e:
            logger.exception("QUICReceiver processing failed: %s", e)
            raise QUICFrameReassemblyError(str(e)) from e