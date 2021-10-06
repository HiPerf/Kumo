using System.Collections;
using System.Collections.Generic;
namespace Kumo
{
    public class WorldUpdateData : Kaminari.IHasDataVector<Kumo.EntityUpdate>
    {
        public void initialize()
        {
            data = new List<Kumo.EntityUpdate>();
        }
        public List<Kumo.EntityUpdate> getData()
        {
            return data;
        }
        public void pack(Kaminari.IMarshal marshal, Kaminari.Packet packet)
        {
            packet.getData().write((byte)this.data.Count);
            foreach (EntityUpdate val in this.data)
            {
                val.pack(marshal, packet);
            }
        }
        public bool unpack(Kaminari.IMarshal marshal, Kaminari.PacketReader packet)
        {
            int size_data = packet.getData().readByte();
            this.data = new List<EntityUpdate>();
            for (int i = 0; i < size_data; ++i)
            {
                EntityUpdate data = new EntityUpdate();
                if (data.unpack(marshal, packet))
                {
                    this.data.Add(data);
                }
                else
                {
                    return false;
                }
            }
            return true;
        }
        public int size(Kaminari.IMarshal marshal)
        {
            int size = 0;
            size += sizeof(byte) + this.data.Count * marshal.size<EntityUpdate>();
            return size;
        }
        public List<EntityUpdate> data;
    }

}
