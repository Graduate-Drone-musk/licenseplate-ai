# License plate detect

<p>
This license plate detection model is a model for Korean License Plate Recognition.
</p>

<br>

## Model process
1. Image capture with camera
2. detect carplate using yolo5
3. Image crop
4. Text detect using CRAFT
5. Text Recognize usig "TPS-VGG-BiLSTM-CTC"

<img src="./figures/lp_process.png" width="1000" title="Model process">



