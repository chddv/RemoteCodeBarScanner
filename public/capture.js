(
  function()
  {

    function log(msg)
    {
      var brnode = document.createElement('BR');
      dvLog.insertBefore(brnode, dvLog.childNodes[0]);
      var textnode = document.createTextNode(msg); 
      dvLog.insertBefore(textnode, dvLog.childNodes[0]);
      console.log(msg);
    }

    var _scannerIsRunning = false;
    function startup()
    {
      log("startup!");
      Quagga.init(
      {
        inputStream: {
            name: "Live",
            type: "LiveStream",
            //target: document.getElementById('camera'), ===> not working ???
            constraints: {
                width: 480,
                height: 320,
                facingMode: "environment"
            },
        },
        decoder: {
            readers: [
                "code_128_reader",
                "ean_reader",
                "ean_8_reader",
                "code_39_reader",
                "code_39_vin_reader",
                "codabar_reader",
                "upc_reader",
                "upc_e_reader",
                "i2of5_reader"
            ],
            debug: {
                showCanvas: true,
                showPatches: true,
                showFoundPatches: true,
                showSkeleton: true,
                showLabels: true,
                showPatchLabels: true,
                showRemainingPatchLabels: true,
                boxFromPatches: {
                    showTransformed: true,
                    showTransformedBox: true,
                    showBB: true
                }
            }
        },
      },
      function (err)
      {
        log("Quagga Event Error");
        if (err) {
            log(err);
            return;
        }

        log("Quagga Initialization finished. Ready to start");
        Quagga.start();

        _scannerIsRunning = true;
      }); // end of init Quagga

      Quagga.onProcessed(function (result) {
        var drawingCtx = Quagga.canvas.ctx.overlay,
        drawingCanvas = Quagga.canvas.dom.overlay;

        if (result) {
            if (result.boxes) {
                drawingCtx.clearRect(0, 0, parseInt(drawingCanvas.getAttribute("width")), parseInt(drawingCanvas.getAttribute("height")));
                result.boxes.filter(function (box) {
                    return box !== result.box;
                }).forEach(function (box) {
                    Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, drawingCtx, { color: "green", lineWidth: 2 });
                });
            }

            if (result.box) {
                Quagga.ImageDebug.drawPath(result.box, { x: 0, y: 1 }, drawingCtx, { color: "#00F", lineWidth: 2 });
            }

            if (result.codeResult && result.codeResult.code) {
                Quagga.ImageDebug.drawPath(result.line, { x: 'x', y: 'y' }, drawingCtx, { color: 'red', lineWidth: 3 });
            }
        }
      }); // end of Quagga onProcess

      Quagga.onDetected(function (result) {
          log("Barcode detected and processed : [" + result.codeResult.code + "]", result);          
          Quagga.stop();
          _scannerIsRunning = false;
      });
    }  // end of startup

    // Start/stop scanner
    document.getElementById("btnScan").addEventListener("click", 
      function () {
        if (_scannerIsRunning) {
          log("stop Quagga from button");
          Quagga.stop();
        } else {
          log("start Quagga from button");
          Quagga.start();
        }
      },
      false
    );

    // Set up our event listener to run the startup process
    // once loading is complete.
    window.addEventListener('load', startup, false);
  }    
)();