using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class RelicButton : MonoBehaviour
{
    [SerializeField] private Calculator calculator;
    [SerializeField] private Dropdown classes;
    [SerializeField] private Dropdown levels;
    [SerializeField] private TextMeshProUGUI display;
    [SerializeField] private int position;

    // Update is called once per frame
    public void Update()
    {
        if (calculator == null || calculator.Relics == null)
        {
            Debug.LogError("Calculator or Relics are null");
            return;
        }
        
        // Debug.Log(classes.value);
        display.text = calculator.Relics.Branches[classes.captionText.text].LevelBranches[Int32.Parse(levels.captionText.text)].Positions[position].Name;
    }
}
