using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class Success : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
            {
                return false;
            }
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            return size;
        }
    }

}
