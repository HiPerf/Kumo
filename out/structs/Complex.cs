using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class Complex : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write(this.x.hasValue());
            if (this.x.hasValue())
            {
                packet.getData().write((uint)this.x.getValue());
            }
            packet.getData().write((byte)this.y.Count);
            foreach (SpawnData val in this.y)
            {
                val.pack(marshal, packet);
            }
            packet.getData().write((int)this.z);
            packet.getData().write(this.w.hasValue());
            if (this.w.hasValue())
            {
                packet.getData().write((byte)this.w.getValue().Count);
                foreach (bool val in this.w.getValue())
                {
                    packet.getData().write((bool)val);
                }
            }
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + sizeof(byte) > packet.bufferSize())
            {
                return false;
            }
            this.x = new Kaminari.Optional<uint>();
            if (packet.getData().readByte() == 1)
            {
                if (packet.bytesRead() + marshal.size<uint>() > packet.bufferSize())
                {
                    return false;
                }
                this.x.setValue(packet.getData().readUint());
            }
            int size_y = packet.getData().readByte();
            this.y = new List<SpawnData>();
            for (int i = 0; i < size_y; ++i)
            {
                SpawnData data = new SpawnData();
                if (data.unpack(marshal, packet))
                {
                    this.y.Add(data);
                }
                else
                {
                    return false;
                }
            }
            if (packet.bytesRead() + marshal.size<int>() > packet.bufferSize())
            {
                return false;
            }
            this.z = packet.getData().readInt();
            if (packet.bytesRead() + sizeof(byte) > packet.bufferSize())
            {
                return false;
            }
            this.w = new Kaminari.Optional<List<bool>>();
            if (packet.getData().readByte() == 1)
            {
                int size_w = packet.getData().readByte();
                if (packet.bytesRead() + size_w * marshal.size<bool>() > packet.bufferSize())
                {
                    return false;
                }
                this.w.setValue(new List<bool>());
                for (int i = 0; i < size_w; ++i)
                {
                    this.w.getValue().Add(packet.getData().readBool());
                }
            }
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += sizeof(byte);
            if (this.x.hasValue())
            {
                size += marshal.size<uint>();
            }
            size += sizeof(byte) + this.y.Count * marshal.size<SpawnData>();
            size += marshal.size<int>();
            size += sizeof(byte);
            if (this.w.hasValue())
            {
                size += sizeof(byte) + this.w.getValue().Count * marshal.size<bool>();
            }
            return size;
        }
        public Kaminari.Optional<uint> x;
        public List<SpawnData> y;
        public int z;
        public Kaminari.Optional<List<bool>> w;
    }

}
