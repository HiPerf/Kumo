class ProtocolQueues
{
    public  ProtocolQueues(int resendThreshold)
    {
        reliable = new ReliableQueue<ImmediatePacker>(ImmediatePacker.class);
        ordered = new ReliableQueue<OrderedPacker>(OrderedPacker.class);
    }
    public void reset()
    {
        reliable.reset();
        ordered.reset();
    }
    public void ack(Short blockId)
    {
        reliable.ack(blockId);
        ordered.ack(blockId);
    }
    public void process(Short blockId, Ref<Short> remaining, TreeMap<Integer, ArrayList<Packet>> byBlock)
    {
        reliable.process(blockId, remaining, byBlock);
        ordered.process(blockId, remaining, byBlock);
    }
    private ReliableQueue<ImmediatePacker> reliable;
    private ReliableQueue<OrderedPacker> ordered;
}

