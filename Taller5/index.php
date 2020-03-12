<?php
// Yes, we know this code is vulnerable.
if( isset( $_POST[ 'prog' ] ) ) {
    if ($_POST[ 'ip' ] != '') {
      $ip = $_POST[ 'ip' ];
      $ip2 = $_POST[ 'ip2' ];
      $cmdln = './' . $_POST['prog'] . ' ' . $ip . ' ' . $ip2; //. ' 2>&1'; 
      $cmd = shell_exec( $cmdln); 
      // $cmd = shell_exec('RET='+$cmdln+';echo $RET');
    }
    
    $source_name = $_POST['prog'] . '.c';
    $fh = fopen($source_name, 'r') or die('Could not open file'. $php_errormsg);
    $fcontents = fread($fh, filesize($source_name));   
}
?> 

<html>
<head>
<title>Secure Coding: C/C++ Vulnerability Tutorial</title>
</head>
<body>
	<h2>Secure Coding: C/C++ Vulnerability Tutorial</h2>
	
	<form name="myform" id="myform" method="post">
	Step 1: Select an executable from the list: 
	<select name="prog" id="prog" onchange="this.form.submit()">
	  <option value="s11ccodeexample">---</option>
      <option value="s19strcopystrcat">s19strcopystrcat</option>
      <option value="s20strcopystrcatfixed">s20strcopystrcatfixed</option>
      <option value="s21offbyone">s21offbyone</option>
      <option value="s22nulltermination">s22nulltermination</option>
      <option value="s23strtruncation">s23strtruncation</option>
      <option value="s24strerrwofunctions">s24strerrwofunctions</option>
      <option value="s27meminiterror">s27meminiterror</option>
      <option value="s35integeroverflow">s35integeroverflow</option>
      <option value="s36signerror">s36signerror</option>
      <option value="s37truncationerror">s37truncationerror</option>
      <option value="s38bufferoverflow">s38bufferoverflow</option>
      <option value="s39initlogicerror">s39initlogicerror</option>
      <option value="s43formatstrbo">s43formatstrbo</option>
      <option value="s44readingstackmem">s44readingstackmem</option>
      <option value="s45writememformatstr">s45writememformatstr</option>
      <option value="s46overwrarbitrarymem">s46overwrarbitrarymem</option>
	</select>
	<br>
	Step 2: Provide 1 or 2 input arguments:	
	<input type="textfield" name="ip" id="ip">
	<input type="textfield" name="ip2" id="ip2">
	<br>
	Step 3: Click on <input type="submit" name="execute" id="execute" value="execute">
	</form>
	<h2>Source Code:</h2>
	<pre><?php echo $fcontents; ?></pre>
	<h2>Executed Command:</h2>
	<pre><?php echo $cmdln; ?></pre>
	<h2>Console Ouput:</h2>
	<pre><?php echo $cmd; ?></pre>
</body>
<script>
var temp = "<?php echo $_POST[ 'prog' ];?>";
var mySelect = document.getElementById('prog');

for(var i, j = 0; i = mySelect.options[j]; j++) {
    if(i.value == temp) {
        mySelect.selectedIndex = j;
        break;
    }
}
</script>
</html>
