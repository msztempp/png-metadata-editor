# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
# 
# 
# def compute_dft(channel):
#     img_float32 = np.float32(channel)
#     dft = cv2.dft(img_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
#     dft_shift = np.fft.fftshift(dft)
#     return dft_shift
# 
# 
# # magnitude and phase, 20*log(|G(jw)|), 20*log(Arg(G(jw)))
# def compute_magnitude_and_phase(dft_shift):
#     magnitude_spectrum, phase_spectrum = 20 * np.log(cv2.cartToPolar(dft_shift[:, :, 0], dft_shift[:, :, 1]))
#     return magnitude_spectrum, phase_spectrum
# 
# 
# def perform_fft(img_file):
#     # Load image
#     img = cv2.imread(img_file)
# 
#     # Split channels
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     blue_channel, green_channel, red_channel = cv2.split(img)
# 
#     # Compute DFT and magnitude/phase for each channel
#     channels = [(gray, 'Gray'), (red_channel, 'Red'), (green_channel, 'Green'), (blue_channel, 'Blue')]
#     magnitude_spectrums = []
#     phase_spectrums = []
# 
#     for channel, channel_name in channels:
#         dft_shift = compute_dft(channel)
#         magnitude_spectrum, phase_spectrum = compute_magnitude_and_phase(dft_shift)
#         magnitude_spectrums.append(magnitude_spectrum)
#         phase_spectrums.append(phase_spectrum)
# 
#         # Display magnitude and phase
#         plt.figure(channel_name + " channel")
#         plt.subplot(121), plt.imshow(magnitude_spectrum, cmap='gray')
#         plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
#         plt.subplot(122), plt.imshow(phase_spectrum, cmap='gray')
#         plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])
# 
#     plt.show()
# 
#     cv2.waitKey(0)
#     # cv2.destroyAllWindows()
