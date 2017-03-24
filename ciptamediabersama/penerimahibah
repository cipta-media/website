---
title: Pendaftar Hibah
layout: info
---

  <!-- jPages -->
  <script src= "/static/js/jPages.js"></script>
  <script src= "/static/js/js.js"></script>
  <!--<script id= "dsq-count-scr" src="//jalpc.disqus.com/count.js" async></script>-->
  <script>
	/* when document is ready */
	$(function() {
		/* initiate plugin */
		$("#holder").jPages({
			containerID : "itemContainer",
			perPage : 9,
			startPage: 1,
			startRange: 1,
			midRange: 3,
			endRange: 1
		});
	});
  </script>
  <!-- jPages -->

<div class="container">

    <div class="row m-b-lg">
        <div class="col-lg-12 text-center">
            <div class="navy-line"></div>
            <h1>Penerima Hibah</h1>
        </div>
    </div>
	<br/>
    <div class="row">	
        {% for hibahcmb in site.data.penerimacmb %}
        {% assign loopindex = forloop.index | modulo: 3 %}
                <div class="col-md-4">
                  <div class="col-md-12 well well-lg" style="height: 600px;">
                  <a href="{{ penerimacmb.link }}"><img class="img-responsive center-block" src="{{ penerimacmb.gambar }}"></a>
                      <hr>
                  <a href="{{ penerimacmb.link }}"><h4>{{ penerimacmb.nomor }} - {{ penerimacmb.judul | truncatewords: 10 }}</h4></a><br/>
                      {{ penerimacmb.deskripsi | truncatewords: 20 }}
                  <hr>
                  <i class="fa fa-map-marker" aria-hidden="true"></i> {{ penerimacmb.lokasi }}
                  </div>
                </div>
                {% endfor %}
	</div>
    <div class="row m-b-lg text-center">
        <div class="col-md-12">
            <div class="pag-holder" id="holder"></div>
        </div>
    </div>
</div>
