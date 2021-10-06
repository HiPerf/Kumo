using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class CharacterSelection : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((byte)this.index);
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
            {
                return false;
            }
            this.index = packet.getData().readByte();
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += marshal.size<byte>();
            return size;
        }
        public byte index;
    }

}
