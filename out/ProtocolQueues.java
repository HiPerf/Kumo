package net.lostsocket.lostsouls.engine.net.kumo;
import java.util.ArrayList;
import java.util.TreeMap;
import net.lostsocket.lostsouls.engine.net.Constants;
import net.lostsocket.lostsouls.engine.net.IAckCallback;
import net.lostsocket.lostsouls.engine.net.Overflow;
import net.lostsocket.lostsouls.engine.net.Packet;
import net.lostsocket.lostsouls.engine.net.Ref;
class ProtocolQueues
{
    public  ProtocolQueues(int resendThreshold)
    {
        reliable = new ReliableQueue<ImmediatePacker>(new ImmediatePacker());
        ordered = new ReliableQueue<OrderedPacker>(new OrderedPacker());
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
    public void sendReliable(Short opcode, IData data, IAckCallback callback)
    {
        reliable.add(opcode, data, callback);
    }
    public void sendReliable(Short opcode, IData data)
    {
        reliable.add(opcode, data);
    }
    public void sendReliable(Packet packet)
    {
        reliable.add(packet);
    }
    public void sendOrdered(Short opcode, IData data, IAckCallback callback)
    {
        ordered.add(opcode, data, callback);
    }
    public void sendOrdered(Short opcode, IData data)
    {
        ordered.add(opcode, data);
    }
    public void sendOrdered(Packet packet)
    {
        ordered.add(packet);
    }
    private ReliableQueue<ImmediatePacker> reliable;
    private ReliableQueue<OrderedPacker> ordered;
}

