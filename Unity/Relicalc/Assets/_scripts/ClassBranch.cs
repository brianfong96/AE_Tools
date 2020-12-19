using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ClassBranch : MonoBehaviour
{
    [SerializeField] public Dictionary<int, LevelBranch> LevelBranches;

    public ClassBranch()
    {
        LevelBranches = new Dictionary<int, LevelBranch>();        
    }    
}
