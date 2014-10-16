<?php

include "../../../inc/includes.php";

error_reporting( E_ALL  );
ini_set("display_errors", 'stderr');
ini_set("log_errors", true);

$agent = new PluginFusioninventoryAgent();

echo "-> Testing agent->getAgentsFromComputers(array()) \n";
echo "Result: ". count($agent->getAgentsFromComputers(array()));
echo "\n";

$group = new PluginFusioninventoryDeployGroup();

$id_group = 2;
$group->getFromDB($id_group);

echo "-> Testing Dynamic Group '".$group->fields['name']."(".$group->fields['id'].")' \n";

$targets = PluginFusioninventoryDeployGroup::getTargetsForGroup($group);
$search_params = PluginFusioninventoryDeployGroup::getSearchParamsAsAnArray($group, false,true);
print_r($search_params);
print_r("Targets: " . count($targets) ."\n");

