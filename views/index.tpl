<html>

	<body>
		<div class="container cameras">
			<h3>Cameras</h3>
			% for item in cameras:
			<div><a href="/{{item}}/">{{item}}</a></div>
			% end
		</div>
		<div class="container controls">
			<h3>Controls</h3>
			<a href="/recycle">Refresh Camera List</a>
		</div>
	</body>

</html>