using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class Character : Kaminari.IData
    {
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((string)this.name);
            packet.getData().write((ushort)this.level);
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            if (packet.bytesRead() + marshal.size<byte>() > packet.bufferSize())
            {
                return false;
            }
            if (packet.bytesRead() + marshal.size<byte>() + packet.getData().peekByte() > packet.bufferSize())
            {
                return false;
            }
            this.name = packet.getData().readString();
            if (packet.bytesRead() + marshal.size<ushort>() > packet.bufferSize())
            {
                return false;
            }
            this.level = packet.getData().readUshort();
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += marshal.size<byte>() + this.name.Length;
            size += marshal.size<ushort>();
            return size;
        }
        public string name;
        public ushort level;
    }

}
