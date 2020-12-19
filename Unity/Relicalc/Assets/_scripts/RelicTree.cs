using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RelicTree
{
    public Dictionary<string, ClassBranch> Branches { get; }
    public Dictionary<int, Relic> IdToRelics { get; }
    public  Dictionary<string, int> NameToId { get; }

    public RelicTree(string tsv, Dictionary<int, Relic> relics)
    {
        IdToRelics = relics;
        NameToId = new Dictionary<string, int>();
        foreach (var id in IdToRelics.Keys)
        {
            NameToId[IdToRelics[id].Name] = id;
        }
        Branches = new Dictionary<string, ClassBranch>();
        var rows = tsv.Split('\n');

        for (int i = 1; i < rows.Length; i++)
        {
            var row = rows[i].Split('\t');
            var classBranch = row[0];
            var level = Int32.Parse(row[1]);
            var r1 = IdToRelics[Int32.Parse(row[2])];
            var r2 = IdToRelics[Int32.Parse(row[4])];
            var r3 = IdToRelics[Int32.Parse(row[6])];
            var r4 = IdToRelics[Int32.Parse(row[8])];
            var r5 = IdToRelics[Int32.Parse(row[10])];
            var r6 = IdToRelics[Int32.Parse(row[12])];
            
            if (!Branches.ContainsKey(classBranch))
            {
                Branches[classBranch] = new ClassBranch();
            }

            Branches[classBranch].LevelBranches[level] = new LevelBranch(r1, r2, r3, r4, r5, r6);                        
        }
    }
}
