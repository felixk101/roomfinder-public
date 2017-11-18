/*
* functions.js
* Includes required functions for index.html
*/

/*
* Function allBuildingsSelected
* checks and unchecks all buildings checkboxes according to its state
* */
function allBuildingsSelected()
{
    var AllBuildingsCheckbox = document.getElementById("allBuildings");
    document.getElementById("buildingA").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingB").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingC").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingD").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingE").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingF").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingG").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingH").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingJ").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingKLM").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingN").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingP").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingR").checked = AllBuildingsCheckbox.checked;
    document.getElementById("buildingW").checked = AllBuildingsCheckbox.checked;
}

/*
* Function oneBuildingDeselected(id)
* Parameter: id of the checkbox which is clicked
* if checkbox is unchecked allBuildings checkbox is unchecked too
* if checkbox is checked all checkboxes of the buildings are tested and if they are checked allBuildings
* checkbox is checked otherwise nothing happens
 */
function oneBuildingDeselected(id)
{
    if (document.getElementById(id).checked == false)
    {
        document.getElementById("allBuildings").checked = false;
    }
    else
    {
        if (document.getElementById("buildingA").checked && document.getElementById("buildingB").checked
              && document.getElementById("buildingC").checked
              && document.getElementById("buildingD").checked
              && document.getElementById("buildingE").checked
              && document.getElementById("buildingF").checked
              && document.getElementById("buildingG").checked
              && document.getElementById("buildingH").checked
              && document.getElementById("buildingJ").checked
              && document.getElementById("buildingKLM").checked
              && document.getElementById("buildingN").checked
              && document.getElementById("buildingP").checked
              && document.getElementById("buildingR").checked
              && document.getElementById("buildingW").checked
            )
        {
            document.getElementById("allBuildings").checked = true;
        }
    }
}

/*
* Function allLevelSelected
* checks and unchecks all level checkboxes according to its state
* */
function allLevelSelected()
{
    var AllLevelCheckbox = document.getElementById("allLevel");
    document.getElementById("firstLevel").checked = AllLevelCheckbox.checked;
    document.getElementById("secondLevel").checked = AllLevelCheckbox.checked;
    document.getElementById("thirdLevel").checked = AllLevelCheckbox.checked;
    document.getElementById("fourthLevel").checked = AllLevelCheckbox.checked;
}

/*
* Function onLevelDeselected(id)
* Parameter: id of the checkbox which is clicked
* if checkbox is unchecked allLevel checkbox is unchecked too
* if checkbox is checked all checkboxes of the level are tested and if they are checked allLevel checkbox
* is checked otherwise nothing happens
 */
function oneLevelDeselected(id)
{
    if (document.getElementById(id).checked == false)
    {
        document.getElementById("allLevel").checked = false;
    }
    else
    {
        if (document.getElementById("firstLevel").checked && document.getElementById("secondLevel").checked
              && document.getElementById("thirdLevel").checked && document.getElementById("fourthLevel").checked)
        {
            document.getElementById("allLevel").checked = true;
        }
    }
}

/*
* Function verifyCheckboxes()
* verifies if all checkboxes of the buildings and/or all checkboxes of levels are selected already
 */
function verifyCheckboxes()
{
    oneLevelDeselected('firstLevel');
    oneBuildingDeselected('buildingA');
}