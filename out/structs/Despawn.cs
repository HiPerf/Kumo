using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class Despawn : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((ulong)this.id);
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
            {
                return false;
            }
            this.id = packet.getData().readUlong();
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += marshal.size<ulong>();
            return size;
        }
        public ulong id;
    }

}
