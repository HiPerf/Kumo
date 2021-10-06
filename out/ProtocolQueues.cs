using System;
using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class ProtocolQueues : Kaminari.IProtocolQueues
    {
        public  ProtocolQueues(int resendThreshold)
        {
            reliable = new Kaminari.ReliableQueue<Kaminari.ImmediatePacker, Kaminari.Packet>(new Kaminari.ImmediatePacker());
            mostRecent = new Kaminari.ReliableQueueByOpcode<Kaminari.MostRecentPackerByOpcode>(new Kaminari.MostRecentPackerByOpcode());
            ordered = new Kaminari.ReliableQueue<Kaminari.OrderedPacker, Kaminari.Packet>(new Kaminari.OrderedPacker());
            eventuallySynced = new Kaminari.EventuallySyncedQueue<Kaminari.VectorMergePacker<WorldUpdateData, EntityUpdate>, EntityUpdate>(new VectorMergePacker(WorldUpdateData.class, Opcodes.opcodeWorldUpdate));
        }
        public void reset()
        {
            reliable.clear();
            mostRecent.clear();
            ordered.clear();
            eventuallySynced.clear();
        }
        public void ack(ushort blockId)
        {
            reliable.ack(blockId);
            mostRecent.ack(blockId);
            ordered.ack(blockId);
            eventuallySynced.ack(blockId);
        }
        public void process(ushort blockId, ref ushort remaining, SortedDictionary<uint, List<Kaminari.Packet>> byBlock)
        {
            reliable.process(Marshal.instance, blockId, ref remaining, byBlock);
            mostRecent.process(Marshal.instance, blockId, ref remaining, byBlock);
            ordered.process(Marshal.instance, blockId, ref remaining, byBlock);
            eventuallySynced.process(Marshal.instance, blockId, ref remaining, byBlock);
        }
        public void sendReliable(ushort opcode, Kaminari.IData data, Action callback)
        {
            reliable.add(Marshal.instance, opcode, data, callback);
        }
        public void sendReliable(ushort opcode, Kaminari.IData data)
        {
            reliable.add(Marshal.instance, opcode, data, null);
        }
        public void sendReliable(Kaminari.Packet packet)
        {
            reliable.add(packet);
        }
        public void sendMostRecent(ushort opcode, Kaminari.IData data, Action callback)
        {
            mostRecent.add(Marshal.instance, opcode, data, callback);
        }
        public void sendMostRecent(ushort opcode, Kaminari.IData data)
        {
            mostRecent.add(Marshal.instance, opcode, data, null);
        }
        public void sendOrdered(ushort opcode, Kaminari.IData data, Action callback)
        {
            ordered.add(Marshal.instance, opcode, data, callback);
        }
        public void sendOrdered(ushort opcode, Kaminari.IData data)
        {
            ordered.add(Marshal.instance, opcode, data, null);
        }
        public void sendOrdered(Kaminari.Packet packet)
        {
            ordered.add(packet);
        }
        public void sendEventuallySynced(ushort opcode, Kaminari.IData data)
        {
            eventuallySynced.add(Marshal.instance, opcode, data, null);
        }
        private Kaminari.ReliableQueue<Kaminari.ImmediatePacker, Kaminari.Packet> reliable;
        private Kaminari.ReliableQueueByOpcode<Kaminari.MostRecentPackerByOpcode> mostRecent;
        private Kaminari.ReliableQueue<Kaminari.OrderedPacker, Kaminari.Packet> ordered;
        private Kaminari.EventuallySyncedQueue<Kaminari.VectorMergePacker<WorldUpdateData, EntityUpdate>, EntityUpdate> eventuallySynced;
    }

}
