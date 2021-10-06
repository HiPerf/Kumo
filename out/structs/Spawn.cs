using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class Spawn : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((ulong)this.id);
            packet.getData().write((ushort)this.type);
            packet.getData().write((float)this.x);
            packet.getData().write((float)this.z);
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
            {
                return false;
            }
            this.id = packet.getData().readUlong();
            this.type = packet.getData().readUshort();
            this.x = packet.getData().readFloat();
            this.z = packet.getData().readFloat();
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += marshal.size<ulong>();
            size += marshal.size<ushort>();
            size += marshal.size<float>();
            size += marshal.size<float>();
            return size;
        }
        public ulong id;
        public ushort type;
        public float x;
        public float z;
    }

}
