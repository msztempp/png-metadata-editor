import cv2
import numpy as np
from matplotlib import pyplot as plt

# load image
img = cv2.imread('../img-example/lena.png')

# load image into graystyle and rgb channels
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blueChannel = img[:, :, 0]
greenChannel = img[:, :, 1]
redChannel = img[:, :, 2]

# dft of every image's part
# gray
imgFloat32 = np.float32(gray)
dftGray = cv2.dft(imgFloat32, flags=cv2.DFT_COMPLEX_OUTPUT)
dftShiftGray = np.fft.fftshift(dftGray)

# redChannel
imgFloat32 = np.float32(redChannel)
dftRedChannel = cv2.dft(imgFloat32, flags=cv2.DFT_COMPLEX_OUTPUT)
dftShiftRedChannel = np.fft.fftshift(dftRedChannel)

# greenChannel
imgFloat32 = np.float32(greenChannel)
dftGreenChannel = cv2.dft(imgFloat32, flags=cv2.DFT_COMPLEX_OUTPUT)
dftShiftGreenChannel = np.fft.fftshift(dftGreenChannel)

# blueChannel
imgFloat32 = np.float32(blueChannel)
dftBlueChannel = cv2.dft(imgFloat32, flags=cv2.DFT_COMPLEX_OUTPUT)
dftShiftBlueChannel = np.fft.fftshift(dftBlueChannel)

# magnitude and phase, 20*log(|G(jw)|), 20*log(Arg(G(jw)))
magnitudeSpectrumGray, phaseSpectrumGray = 20 * np.log(cv2.cartToPolar(dftShiftGray[:, :, 0], dftShiftGray[:, :, 1]))
magnitudeSpectrumRedChannel, phaseSpectrumRedChannel = 20 * np.log(cv2.cartToPolar(dftShiftRedChannel[:, :, 0], dftShiftRedChannel[:, :, 1]))
magnitudeSpectrumGreenChannel, phaseSpectrumGreenChannel = 20 * np.log(cv2.cartToPolar(dftShiftGreenChannel[:, :, 0], dftShiftGreenChannel[:, :, 1]))
magnitudeSpectrumBlueChannel, phaseSpectrumBlueChannel = 20 * np.log(cv2.cartToPolar(dftShiftBlueChannel[:, :, 0], dftShiftBlueChannel[:, :, 1]))

print(magnitudeSpectrumGray.ndim)

# display magnitude and phase
plt.figure("Gray image")
plt.subplot(121), plt.imshow(magnitudeSpectrumGray, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(phaseSpectrumGray, cmap='gray')
plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])

plt.figure("Red channel")
plt.subplot(121), plt.imshow(magnitudeSpectrumRedChannel, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(phaseSpectrumRedChannel, cmap='gray')
plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])

plt.figure("Green channel")
plt.subplot(121), plt.imshow(magnitudeSpectrumGreenChannel, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(phaseSpectrumGreenChannel, cmap='gray')
plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])

plt.figure("Blue channel")
plt.subplot(121), plt.imshow(magnitudeSpectrumBlueChannel, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(phaseSpectrumBlueChannel, cmap='gray')
plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])

plt.show()

cv2.waitKey(0)
# cv2.destroyAllWindows()
