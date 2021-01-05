import java.util.ArrayList;
import java.util.TreeMap;
import net.kaminari.Constants;
import net.kaminari.IAckCallback;
import net.kaminari.NoCallback;
import net.kaminari.IMarshal;
import net.kaminari.IProtocolQueues;
import net.kaminari.packers.IData;
import net.kaminari.Overflow;
import net.kaminari.Packet;
import net.kaminari.Ref;
import net.kaminari.queues.ReliableQueue;
import net.kaminari.queues.UnreliableQueue;
import net.kaminari.queues.EventuallySyncedQueue;
import net.kaminari.packers.ImmediatePacker;
import net.kaminari.packers.OrderedPacker;
import net.kaminari.packers.MergePacker;
import net.kaminari.packers.MostRecentPackerWithId;
public class ProtocolQueues : IProtocolQueues
{
    public  ProtocolQueues(int resendThreshold)
    {
        reliable = new ReliableQueue<ImmediatePacker, Packet>(new ImmediatePacker());
        ordered = new ReliableQueue<OrderedPacker, Packet>(new OrderedPacker());
    }
    public void reset()
    {
        reliable.clear();
        ordered.clear();
    }
    public void ack(ushort blockId)
    {
        reliable.ack(blockId);
        ordered.ack(blockId);
    }
    public void process(ushort blockId, ref ushort remaining, SortedDictionary<uint, List<Packet>> byBlock)
    {
        reliable.process(Marshal.instance, blockId, remaining, byBlock);
        ordered.process(Marshal.instance, blockId, remaining, byBlock);
    }
    public void sendReliable(ushort opcode, IData data, IAckCallback callback)
    {
        reliable.add(Marshal.instance, opcode, data, callback);
    }
    public void sendReliable(ushort opcode, IData data)
    {
        reliable.add(Marshal.instance, opcode, data, new NoCallback());
    }
    public void sendReliable(Packet packet)
    {
        reliable.add(packet);
    }
    public void sendOrdered(ushort opcode, IData data, IAckCallback callback)
    {
        ordered.add(Marshal.instance, opcode, data, callback);
    }
    public void sendOrdered(ushort opcode, IData data)
    {
        ordered.add(Marshal.instance, opcode, data, new NoCallback());
    }
    public void sendOrdered(Packet packet)
    {
        ordered.add(packet);
    }
    private ReliableQueue<ImmediatePacker, Packet> reliable;
    private ReliableQueue<OrderedPacker, Packet> ordered;
}

