from . import boxes


BASE_QUEUES = (
    'reliable_queue', 
    'unreliable_queue',
    'eventually_synced_queue'
)

BASE_PACKERS = (
    'most_recent_packer_by_opcode',
    'most_recent_packer_by_id',
    'most_recent',
    'unique_merge_packer',
    'merge_packer',
    'ordered_packer',
    'immediate_packer'
)

TRIVIAL_TYPES = (
    'int8', 'int16', 'int32', 'int64',
    'uint8', 'uint16', 'uint32', 'uint64',
    'float', 'double',
    'bool'
)

OBJECT_TYPES = ('string', 'vector')
        
def check_queue_base(name, queue):
    subclass = queue.base.subtype.eval()
    cond = subclass in BASE_QUEUES
    assert cond, f'Queue `{name}` subclasses incorrect queue `{subclass}`'

def check_queue_specifier(name, queue, messages, programs):
    queue_type = queue.specifier.queue_type
    if queue_type == boxes.QueueSpecifierType.SPECIALIZED:
        ptype = queue.specifier.args.value
        assert ptype in BASE_PACKERS, f'Queue `{name}` specifies incorrect packer `{ptype}`'

    elif queue_type == boxes.QueueSpecifierType.TEMPLATED:
        gtype, dtype, program = (x.eval() for x in queue.specifier.args)

        assert gtype in messages, f'Queue `{name}` specifies incorrect global message `{gtype}`'
        assert dtype in messages, f'Queue `{name}` specifies incorrect detail message `{dtype}`'
        assert program in programs, f'Queue `{name}` specifies incorrect program `{program}`'
    elif queue_type == boxes.QueueSpecifierType.ARRAY:
        raise NotImplementedError("Array definitions are deprecated")

def check_message_types(name, message, messages):
    for decl in message.fields.eval():
        dtype = decl.dtype.dtype.eval()

        assert dtype in TRIVIAL_TYPES or \
               dtype in OBJECT_TYPES or \
               dtype in messages, f'Message `{name}` uses invalid type `{dtype}`'

        if dtype == 'vector':
            spec = decl.dtype.spec.eval()

            assert spec in TRIVIAL_TYPES or \
                    spec in OBJECT_TYPES or \
                    spec in messages, f'Message `{name}` uses invalid type `{spec}` in vector'
            
def check_program_queue(name, program, queues):
    queue_name = program.queue.eval()
    assert queue_name in queues, f'Program `{name}` specifies incorrect queue `{queue_name}`'

    spec = queues[queue_name].specifier
    if spec.queue_type == boxes.QueueSpecifierType.ARRAY:
        assert queue_obj.idx is not None, f'Message `{name}` does not specify queue index for type `{queue_name}`'
        idx = queue_obj.idx.eval()
        size = spec.args.eval()
        assert idx < size, f'Message `{name}` uses array index {idx} >= {size}'

def check_program_message(name, program, messages):
    for arg in program.args.eval():
        assert arg in messages, f'Program `{name}` specifies incorrect message `{arg}`'

def check_program_arguments(name, program, messages, queues):
    args = program.args.eval()
    if len(args) > 1:
        def get_queue_name(arg):
            message = messages[arg]
            queue = queues[message.block.queue.identifier.eval()]
            return queue.name.eval()

        base_name = get_queue_name(args[0])
        assert all(base_name == get_queue_name(arg) for arg in args), \
            f'Program `{name}` uses messages from different queues, first being `{base_name}`'
