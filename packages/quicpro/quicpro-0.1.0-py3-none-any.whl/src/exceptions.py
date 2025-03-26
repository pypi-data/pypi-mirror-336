class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass

class EncodingError(PipelineError):
    """Exception raised when encoding of a message fails."""
    pass

class EncryptionError(PipelineError):
    """Exception raised during packet encryption failures."""
    pass

class TransmissionError(PipelineError):
    """Exception raised during network transmission issues."""
    pass

class DecryptionError(PipelineError):
    """Exception raised during the decryption process on the receiver side."""
    pass

class HTTP3FrameError(Exception):
    """Custom exception for HTTP/3 frame extraction and validation errors."""
    pass

class DecodingError(PipelineError):
    """Exception raised during the decoding process on the receiver side."""
    pass

class QUICFrameReassemblyError(PipelineError):
    """Exception raised during QUIC frame reassembly."""
    pass