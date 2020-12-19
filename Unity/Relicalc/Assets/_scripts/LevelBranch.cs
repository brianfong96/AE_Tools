using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LevelBranch : MonoBehaviour
{
    [SerializeField] public Dictionary<int, Relic> Positions { get; }
    
    public LevelBranch(Relic r1, Relic r2, Relic r3, Relic r4, Relic r5, Relic r6)
    {
        Positions = new Dictionary<int, Relic>();
        // reference
        // r1   r2
        // r3   r4
        // r5   r6
        Positions[1] = r1;
        Positions[2] = r2;
        Positions[3] = r3;
        Positions[4] = r4;
        Positions[5] = r5;
        Positions[6] = r6;
    }
}
