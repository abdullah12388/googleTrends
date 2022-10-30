var keyword_id = document.getElementById('hidden_id').name
$.ajax({
    type: 'GET',
    dataType: "json",
    url: 'http://127.0.0.1:8000/h/' + keyword_id,
    success: function (data, status, xhr) {
        am5.ready(function() {
            // Create root element
            var root = am5.Root.new("hisDiv");
            // Set themes
            root.setThemes([
              am5themes_Animated.new(root)
            ]);
            // Create chart
            var chart = root.container.children.push(am5xy.XYChart.new(root, {
              panX: true,
              panY: false,
              wheelX: "panX",
              wheelY: "zoomX",
              pinchZoomX:true
            }));
            // Add cursor
            var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {
              behavior: "none"
            }));
            cursor.lineY.set("visible", false);

            // Create axes
            // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
            // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/category-date-axis/
            var xRenderer = am5xy.AxisRendererX.new(root, {});
            xRenderer.labels.template.set("minPosition", 0.01);
            xRenderer.labels.template.set("maxPosition", 0.99);

            var xAxis = chart.xAxes.push(
              am5xy.CategoryDateAxis.new(root, {
                categoryField: "date",
                baseInterval: [{
                  timeUnit: "day",
                  count: 1
                }],
                renderer: xRenderer,
                tooltip: am5.Tooltip.new(root, {})
              })
            );

            var yAxis = chart.yAxes.push(
              am5xy.ValueAxis.new(root, {
                renderer: am5xy.AxisRendererY.new(root, {})
              })
            );


            // Add series
            var series = chart.series.push(am5xy.LineSeries.new(root, {
              name: "Series",
              xAxis: xAxis,
              yAxis: yAxis,
              valueYField: "value",
              categoryXField: "date"
            }));

            var tooltip = series.set("tooltip", am5.Tooltip.new(root, {}));
            tooltip.label.set("text", "{valueY}");

            // Add scrollbar
            // https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/
            chart.set("scrollbarX", am5.Scrollbar.new(root, {
              orientation: "horizontal"
            }));

            function editData(data){
                var dataChart = []
                for(var i =0; i< data.length ;i++){
                    dataChart.push({
                        'date': new Date(data[i]['time_stamp']).getTime(),
                        'value': data[i]['number_of_interest']
                    });
                }
                return dataChart
            }

            // Set data
            var final_data = editData(data)
            series.data.setAll(final_data);
            xAxis.data.setAll(final_data);
            series.set("stroke", am5.color(0x1AC1DD));

            // Make stuff animate on load
            // https://www.amcharts.com/docs/v5/concepts/animations/
            series.appear(1000);
            chart.appear(1000, 100);

        }); // end am5.ready()
    }
});



$.ajax({
    type: 'GET',
    dataType: "json",
    url: 'http://127.0.0.1:8000/r/' + keyword_id,
    success: function (data, status, xhr) {
        am5.ready(function() {
            // Create root
            var root = am5.Root.new("regDiv");

            // Set themes
            root.setThemes([
              am5themes_Animated.new(root)
            ]);

            // Create chart
            var chart = root.container.children.push(am5map.MapChart.new(root, {
              panX: "rotateX",
              panY: "none",
              projection: am5map.geoAlbersUsa(),
              layout: root.horizontalLayout
            }));

            // Create polygon series
            var polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
              geoJSON: am5geodata_usaLow,
              valueField: "value",
              calculateAggregates: true
            }));

            polygonSeries.mapPolygons.template.setAll({
              tooltipText: "{name}: {value}"
            });

            polygonSeries.set("heatRules", [{
              target: polygonSeries.mapPolygons.template,
              dataField: "value",
              min: am5.color(0xff621f),
              max: am5.color(0x661f00),
              key: "fill"
            }]);

            polygonSeries.mapPolygons.template.events.on("pointerover", function(ev) {
              heatLegend.showValue(ev.target.dataItem.get("value"));
            });

            function editData(data){
                var dataChart = []
                for(var i =0; i< data.length ;i++){
                    dataChart.push({
                        'id': data[i]['region_geo_code'],
                        'value': data[i]['region_interest']
                    });
                }
                return dataChart
            }

            var final_data = editData(data)
            polygonSeries.data.setAll(final_data);

            var heatLegend = chart.children.push(am5.HeatLegend.new(root, {
              orientation: "horizontal",
              startColor: am5.color(0x6794DC),
              endColor: am5.color(0xFF621F),
              startText: "Lowest",
              endText: "Highest",
              stepCount: 5
            }));

            heatLegend.startLabel.setAll({
              fontSize: 12,
              fill: heatLegend.get("startColor")
            });

            heatLegend.endLabel.setAll({
              fontSize: 12,
              fill: heatLegend.get("endColor")
            });

            // change this to template when possible
            polygonSeries.events.on("datavalidated", function () {
              heatLegend.set("startValue", polygonSeries.getPrivate("valueLow"));
              heatLegend.set("endValue", polygonSeries.getPrivate("valueHigh"));
            });

        }); // end am5.ready()
    }
});
