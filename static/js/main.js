


$(document).ready(function() {
  const carrosel = $(".carrossel")
  carrosel.slick();
  
  $(chart_id_1).highcharts({
      chart: payload_1ano.chart,
      title: payload_1ano.title,
      xAxis: payload_1ano.xAxis,
      yAxis: payload_1ano.yAxis,
      series: payload_1ano.series
  });
  $(chart_id_0).highcharts({
      chart: payload_24h.chart,
      title: payload_24h.title,
      xAxis: payload_24h.xAxis,
      yAxis: payload_24h.yAxis,
      series: payload_24h.series
  });
  $(chart_id_2).highcharts({
      chart: payload_1mes.chart,
      title: payload_1mes.title,
      xAxis: payload_1mes.xAxis,
      yAxis: payload_1mes.yAxis,
      series: payload_1mes.series
  });
  $(chart_id_3).highcharts({
      chart: payload_1semana.chart,
      title: payload_1semana.title,
      xAxis: payload_1semana.xAxis,
      yAxis: payload_1semana.yAxis,
      series: payload_1semana.series
  });
});