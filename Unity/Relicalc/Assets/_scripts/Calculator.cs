using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Calculator : MonoBehaviour
{
    [SerializeField] private TextAsset relics;
    [SerializeField] private List<Relic> AllRelics;
    // Start is called before the first frame update
    void Start()
    {
        AllRelics = new List<Relic>();
        var rows = relics.text.Split('\n');

        for (int i = 1; i < rows.Length; i++)
        {
            var rawRelic = rows[i].Split('\t');
            var relic = new Relic(rawRelic[0], rawRelic[1], rawRelic[2], rawRelic[3], rawRelic[4]);
            AllRelics.Add(relic);
            Debug.Log(relic.ToString());            
        }

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
