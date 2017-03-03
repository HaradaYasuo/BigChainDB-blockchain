"""Custom exceptions used in the `bigchaindb` package.
"""
from bigchaindb.exceptions import BigchainDBError


class ConfigurationError(BigchainDBError):
    """Raised when there is a problem with server configuration"""


class DatabaseAlreadyExists(BigchainDBError):
    """Raised when trying to create the database but the db is already there"""


class DatabaseDoesNotExist(BigchainDBError):
    """Raised when trying to delete the database but the db is not there"""


class StartupError(BigchainDBError):
    """Raised when there is an error starting up the system"""


class GenesisBlockAlreadyExistsError(BigchainDBError):
    """Raised when trying to create the already existing genesis block"""


class CyclicBlockchainError(BigchainDBError):
    """Raised when there is a cycle in the blockchain"""


class KeypairNotFoundException(BigchainDBError):
    """Raised if operation cannot proceed because the keypair was not given"""


class KeypairMismatchException(BigchainDBError):
    """Raised if the private key(s) provided for signing don't match any of the
    current owner(s)"""


class OperationError(BigchainDBError):
    """Raised when an operation cannot go through"""


################################################################################
# Validation errors


class ValidationError(BigchainDBError):
    """Raised if there was an error in validation"""


class DoubleSpend(ValidationError):
    """Raised if a double spend is found"""


class InvalidHash(ValidationError):
    """Raised if there was an error checking the hash for a particular
    operation"""


class SchemaValidationError(ValidationError):
    """Raised if there was any error validating an object's schema"""


class InvalidSignature(ValidationError):
    """Raised if there was an error checking the signature for a particular
    operation"""


class ImproperVoteError(ValidationError):
    """Raised if a vote is not constructed correctly, or signed incorrectly"""


class MultipleVotesError(ValidationError):
    """Raised if a voter has voted more than once"""


class TransactionNotInValidBlock(ValidationError):
    """Raised when a transfer transaction is attempting to fulfill the
    outputs of a transaction that is in an invalid or undecided block"""


class AssetIdMismatch(ValidationError):
    """Raised when multiple transaction inputs related to different assets"""


class AmountError(ValidationError):
    """Raised when there is a problem with a transaction's output amounts"""


class TransactionDoesNotExist(ValidationError):
    """Raised if the transaction is not in the database"""


class TransactionOwnerError(ValidationError):
    """Raised if a user tries to transfer a transaction they don't own"""


class SybilError(ValidationError):
    """If a block or vote comes from an unidentifiable node"""
