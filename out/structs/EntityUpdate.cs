using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class EntityUpdate : Kaminari.IHasId
    {
        public ulong getId()
        {
            return id;
        }
        public void setId(ulong id)
        {
            this.id = id;
        }
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((ulong)this.id);
            packet.getData().write((float)this.x);
            packet.getData().write((float)this.z);
            packet.getData().write((float)this.speed);
            packet.getData().write((float)this.vx);
            packet.getData().write((float)this.vz);
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
            {
                return false;
            }
            this.id = packet.getData().readUlong();
            this.x = packet.getData().readFloat();
            this.z = packet.getData().readFloat();
            this.speed = packet.getData().readFloat();
            this.vx = packet.getData().readFloat();
            this.vz = packet.getData().readFloat();
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += marshal.size<ulong>();
            size += marshal.size<float>();
            size += marshal.size<float>();
            size += marshal.size<float>();
            size += marshal.size<float>();
            size += marshal.size<float>();
            return size;
        }
        public ulong id;
        public float x;
        public float z;
        public float speed;
        public float vx;
        public float vz;
    }

}
