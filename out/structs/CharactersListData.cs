using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class CharactersListData : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((byte)this.num_characters);
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
            {
                return false;
            }
            this.num_characters = packet.getData().readByte();
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += marshal.size<byte>();
            return size;
        }
        public byte num_characters;
    }

}
