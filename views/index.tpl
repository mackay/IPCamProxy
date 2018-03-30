<html>

    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

        <!-- Optional theme -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

        <style>
            @media (max-width: 767px) {
                .text-xs-center {
                    text-align: center;
                }
            }

            .floor {
                margin-bottom: 25px;
            }
        </style>
    </head>

    <body>
        <div class="container cameras">
            <h3>Cameras</h3>

            % for item in cameras:
            <div class="row floor text-xs-center">
                <div class="col-sm-3">
                    <a href="/{{item}}/">{{item}}</a>
                </div>
                <div class="col-sm-9">
                    <a class="te" href="/frames/{{item}}.jpg" target="_blank">
                        <img src="./frames/{{item}}_thumbnail.jpg">
                    </a>
                </div>
            </div>
            % end
        </div>
        <div class="container controls">
            <h3>Controls</h3>
            <a href="/recycle">Refresh Camera List</a>
        </div>
    </body>

    <script type="text/javascript">
    $(function() {
        function makeid() {
          var text = "";
          var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

          for (var i = 0; i < 5; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));

          return text;
        }

        function reload_img_src() {
            $("img").each(function(idx, el) {
                var src = $(el).attr("src");
                src = src.split("?")[0] + "?" + makeid();
                $(el).attr("src", src);
            });
        }

        setInterval(function(){ reload_img_src() }, 15 * 1000);
    });
    </script>
</html>