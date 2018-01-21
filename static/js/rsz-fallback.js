var images = $('.rsz-fallback')

images.on('error', function() {
  var image = $(this)
  var src = image.attr('src')

  if (~src.indexOf('.rsz.io')) {
    image.attr('src', src.replace('.rsz.io', ''))
  }
})
