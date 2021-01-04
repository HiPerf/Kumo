import hashlib
from enum import Enum

from .boxes import Direction, QueueSpecifierType


class Role(Enum):
    SERVER = 0
    CLIENT = 1

class Generator(object):
    def __init__(self, config, role, queues, messages, programs):
        # Parser data
        self.config = config
        self.role = role
        self.queues = queues
        self.queue_usage = {queue: 0 for queue in queues}
        self.messages = messages
        self.programs = programs

        # Generated data
        self.opcodes = {}
        self.structures = {}
        self.base_structures = {}
        self.message_packer = {}
        self.message_unpacker = {}
        self.message_size = {}
        self.generated_programs = []
        self.recv_list = []
        self.send_list = []

    # To be implemented by specific language generators
    def _base_message_fields(self, base):
        raise NotImplementedError()

    def _generate_structure(self, message):
        raise NotImplementedError()

    def _generate_base_structure(self, base):
        raise NotImplementedError()

    def _generate_message_packer(self, message):
        raise NotImplementedError()

    def _generate_message_unpacker(self, message):
        raise NotImplementedError()

    def _generate_message_size(self, message):
        raise NotImplementedError()

    def _generate_program_send(self, message):
        raise NotImplementedError()

    def _generate_program_recv(self, message):
        raise NotImplementedError()

    def _generate_internals(self):
        pass

    def _generate_version(self, version):
        raise NotImplementedError()

    def dump(self, path):
        raise NotImplementedError()


    # Generates a deterministic (given the same inputs in the same order) opcode from a name
    def get_opcode(self, program_name):
        if program_name in self.opcodes:
            return self.opcodes[program_name]

        def get_digest(h, encoded):
            h.update(encoded)
        
            # Keep higher most byte reserved for encryption flag
            digest = bytearray(h.digest())
            digest[0] = digest[0] & (~(1 << 7))
            digest = bytearray.hex(digest)
            return digest
        
        encoded = program_name.encode('utf-8')
        h = hashlib.blake2b(digest_size=2)
        digest = get_digest(h, encoded)
        while digest in self.opcodes.values():
            digest = get_digest(h, encoded)

        self.opcodes[program_name] = digest
        return digest

    def is_message(self, dtype):
        return dtype in self.messages
    
    def is_program_sender(self, direction):
        return (self.role == Role.CLIENT and direction == Direction.C2S) or \
            (self.role == Role.SERVER and direction == Direction.S2C)

    def message_fields_including_base(self, message):
        fields = message.fields.eval()

        if message.base.name is not None:
            base = message.base.name.eval()
            if self.is_message(base):
                return self.message_fields_including_base(self.messages[base]) + fields
            else:
                return self._base_message_fields(base) + fields

        return fields

    def can_queue_have_callback(self, queue):
        # Standard queues are IMMEDIATE packers, which means they can have callbacks
        if queue.specifier.queue_type == QueueSpecifierType.STANDARD:
            return True

        if queue.specifier.queue_type == QueueSpecifierType.SPECIALIZED:
            packer = queue.specifier.args.eval()
            return packer in ('immediate_packer', 'ordered_packer', 'most_recent_packer_by_opcode',
                'most_recent_packer_by_id')
            
        return False
        
    def has_queue_packed_add(self, queue):
        # Standard queues are IMMEDIATE packers, which means they can have callbacks
        if queue.specifier.queue_type == QueueSpecifierType.STANDARD:
            return True

        if queue.specifier.queue_type == QueueSpecifierType.SPECIALIZED:
            packer = queue.specifier.args.eval()
            return packer in ('immediate_packer', 'ordered_packer')

        return False

    def get_program_message(self, program):
        args = program.args.eval()
        return args[0]

    def message_inherits_from(self, message, inherits):
        if message.name.eval() == inherits:
            return True

        if message.base.name is not None:
            base = message.base.name.eval()
            # Check here again, not all of them are custom types
            if base == inherits:
                return True

            if self.is_message(base):
                return self.message_inherits_from(self.messages[base], inherits)

        return False

    def generate_structure(self, message):
        message_name = message.name.eval()
        if message_name in self.structures:
            return self.structures[message_name]

        if message.base.name is not None:
            base = message.base.name.eval()
            if self.is_message(base):
                self.generate_structure(self.messages[base])
            else:
                self.generate_base_structure(base)
                assert base in ('has_id', 'has_data_vector'), 'Invalid base class'
        
        struct = self._generate_structure(message)
        self.structures[message_name] = struct
        return struct

    def generate_base_structure(self, base: str):
        if base in self.base_structures:
            return self.base_structures[base]

        self.base_structures[base] = self._generate_base_structure(base)
    
    def generate_message_packer(self, message):
        message_name = message.name.eval()
        if message_name in self.message_packer:
            return self.message_packer[message_name]

        packer = self._generate_message_packer(message)
        self.message_packer[message_name] = packer
        return packer
    
    def generate_message_unpacker(self, message):
        message_name = message.name.eval()
        if message_name in self.message_unpacker:
            return self.message_unpacker[message_name]

        packer = self._generate_message_unpacker(message)
        self.message_unpacker[message_name] = packer
        return packer

    def generate_message_size(self, message):
        message_name = message.name.eval()
        if message_name in self.message_size:
            return self.message_size[message_name]

        method = self._generate_message_size(message)
        self.message_size[message_name] = method
        return method

    def generate_dependable_messages(self, message, packer_or_unpacker):
        for field in self.message_fields_including_base(message):
            message_name = field.dtype.dtype.eval() 
            if message_name == 'vector':
                message_name = field.dtype.spec.eval()
            
            if self.is_message(message_name):
                dependent_message = self.messages[message_name]
                self.generate_structure(dependent_message)
                packer_or_unpacker(dependent_message)
                self.generate_message_size(dependent_message)

    def generate_program(self, program):
        program_name = program.name.eval()

        # Get an opcode for the RPC
        self.get_opcode(program_name)

        # Message packer/unpacker according to direction
        direction = program.direction.eval()
        args = program.args.eval()

        # Update queue_usage
        self.queue_usage[program.queue.eval()] += int(self.is_program_sender(direction))

        assert len(args) == 1, "Multiple arguments have been deprecated"
        message = self.messages[args[0]]

        if direction == Direction.BOTH or \
            (direction == Direction.S2C and self.role == Role.SERVER) or \
            (direction == Direction.C2S and self.role == Role.CLIENT):

            self.generate_structure(message)
            self.generate_message_packer(message)
            self._generate_program_send(program)
            self.send_list.append(program_name)

            self.generate_dependable_messages(message, self.generate_message_packer)

        if direction == Direction.BOTH or \
            (direction == Direction.C2S and self.role == Role.SERVER) or \
            (direction == Direction.S2C and self.role == Role.CLIENT):
            
            self.generate_structure(message)
            self.generate_message_unpacker(message)
            self._generate_program_recv(program)
            self.recv_list.append(program_name)

            self.generate_dependable_messages(message, self.generate_message_unpacker)

        # Message size calculation
        self.generate_message_size(message)

        # Done
        self.generated_programs.append(program_name)

    def generate(self, version):
        for program in self.programs.values():
            self.generate_program(program)

        # Some queues require extra types
        for queue in self.queues.values():
            if queue.specifier.queue_type == QueueSpecifierType.TEMPLATED:
                global_data_name = queue.specifier.args[0].eval()
                message = self.messages[global_data_name]
                
                self.generate_structure(message)
                self.generate_message_packer(message)
                self.generate_message_size(message)

        self._generate_internals()
        self._generate_version(version)
