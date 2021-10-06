using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class SelfUpdate : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((float)this.x);
            packet.getData().write((float)this.z);
            packet.getData().write((float)this.speed);
            packet.getData().write((float)this.vx);
            packet.getData().write((float)this.vz);
            packet.getData().write((byte)this.seq);
            packet.getData().write((ushort)this.frame);
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
            {
                return false;
            }
            this.x = packet.getData().readFloat();
            this.z = packet.getData().readFloat();
            this.speed = packet.getData().readFloat();
            this.vx = packet.getData().readFloat();
            this.vz = packet.getData().readFloat();
            this.seq = packet.getData().readByte();
            this.frame = packet.getData().readUshort();
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += marshal.size<float>();
            size += marshal.size<float>();
            size += marshal.size<float>();
            size += marshal.size<float>();
            size += marshal.size<float>();
            size += marshal.size<byte>();
            size += marshal.size<ushort>();
            return size;
        }
        public float x;
        public float z;
        public float speed;
        public float vx;
        public float vz;
        public byte seq;
        public ushort frame;
    }

}
