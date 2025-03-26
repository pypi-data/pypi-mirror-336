import logging
from typing import Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel, Field, field_validator
from quicpro.exceptions import DecryptionError

logger = logging.getLogger(__name__)


class TLSConfig(BaseModel):
    key: bytes = Field(
        ...,
        min_length=32,
        max_length=32,
        description="32-byte (256-bit) symmetric key for AES-GCM."
    )
    iv: bytes = Field(
        ...,
        min_length=12,
        max_length=12,
        description="12-byte static IV for nonce derivation."
    )

    @field_validator("key")
    def validate_key(cls, v: bytes) -> bytes:
        if len(v) != 32:
            raise ValueError("Key must be exactly 32 bytes (256 bits).")
        return v

    @field_validator("iv")
    def validate_iv(cls, v: bytes) -> bytes:
        if len(v) != 12:
            raise ValueError("IV must be exactly 12 bytes.")
        return v


class TLSDecryptor:
    """
    Production-grade TLSDecryptor that decrypts incoming AES-GCM encrypted UDP datagrams,
    and passes the decrypted QUIC packet to a QUICReceiver.
    The decryption process assumes:
      - The first 8 bytes of the encrypted packet contain the record sequence number (big-endian).
      - The remainder of the packet is the AES-GCM ciphertext.
      - The per-record nonce is computed as:
              nonce = static_iv XOR (sequence_number encoded as 12-byte big-endian)
    Note: In TLS 1.3, the nonces are derived in an identical manner on both sides.
    """
    def __init__(self, quic_receiver: Any, config: TLSConfig) -> None:
        """
        Initializes the TLSDecryptor with a validated TLS configuration.

        Args:
            quic_receiver (Any): An object with a receive(packet: bytes) method.
            config (TLSConfig): TLS configuration containing the encryption key and IV.
        """
        self.quic_receiver = quic_receiver
        self.config = config
        self.aesgcm = AESGCM(self.config.key)

    def _compute_nonce(self, seq_number: int) -> bytes:
        """
        Computes the per-record nonce using the sequence number and static IV.

        Args:
            seq_number (int): The record sequence number.

        Returns:
            bytes: A 12-byte nonce (static_iv XOR sequence_number).
        """
        seq_bytes = seq_number.to_bytes(12, byteorder='big')
        return bytes(iv_byte ^ seq_byte for iv_byte, seq_byte in zip(self.config.iv, seq_bytes))

    def decrypt(self, encrypted_packet: bytes) -> None:
        """
        Decrypts an incoming encrypted UDP datagram and passes it to the QUIC receiver.
        The encrypted packet must have the format:
          [8-byte sequence number][AES-GCM ciphertext]
        The sequence number is used to re-derive the nonce for decryption.

        Args:
            encrypted_packet (bytes): The UDP datagram containing the encrypted record.

        Raises:
            DecryptionError: If decryption or packet reception fails.
        """
        try:
            if len(encrypted_packet) < 9:
                raise ValueError("Encrypted packet is too short to contain a valid header.")
            seq_number = int.from_bytes(encrypted_packet[:8], byteorder='big')
            ciphertext = encrypted_packet[8:]
            nonce = self._compute_nonce(seq_number)
            quic_packet = self.aesgcm.decrypt(nonce, ciphertext, None)
            logger.info("TLSDecryptor decrypted packet with sequence number %d", seq_number)
            self.quic_receiver.receive(quic_packet)
        except Exception as exc:
            logger.exception("TLSDecryptor decryption failed: %s", exc)
            raise DecryptionError(f"TLSDecryptor decryption failed: {exc}") from exc