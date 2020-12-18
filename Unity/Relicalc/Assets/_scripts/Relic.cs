using System;
using System.Collections;
using System.Collections.Generic;

public class Relic
{
    public string Id { get; }
    public string Name { get; }
    public string Quality { get; }
    public int TotalCost { get; }
    public string[] Components { get; }

    public Relic(string id, string name, string quality, string totalCost, string components)
    {
        Id = id;
        Name = name;
        Quality = quality;
        TotalCost = Int32.Parse(totalCost);
        Components = components.Trim().Split(',');
    }

    public override string ToString()
    {
        return $"Id = {Id}\nName = {Name}\nQuality = {Quality}\nTotal Cost = {TotalCost}\nComponents = {string.Join(", ", Components)}";
    }
}
