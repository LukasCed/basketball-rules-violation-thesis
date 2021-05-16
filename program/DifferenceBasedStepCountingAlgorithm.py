    def execute_diff(this, gray1, gray2, made, steps, plot_data):
        if gray1 is not None and gray2 is not None:
            #img1  = flip_img(img1)
            #img2  = flip_img(img2)
            #hsv1 = convert_to_hsv(img1)
            #hsv2 = convert_to_hsv(img2)
            #gray1 = cv2.cvtColor(hsv1, cv2.COLOR_RGB2GRAY)
            #gray2 = cv2.cvtColor(hsv2, cv2.COLOR_RGB2GRAY)
            
            #(score, diff) = compare_ssim(gray1, gray2, full=True)
           # diff = (diff * 255).astype("uint8")
           # thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            thresh = cv2.subtract(gray2, gray1)
            # # cv2.imshow("g1", gray1)
            # # cv2.imshow("g2", gray2)

            # mask upper partition
            height, width = thresh.shape[:2]
            start_row, start_col = int(height * .5), int(0)
            end_row, end_col = int(height), int(width)
            cropped_top = erode(thresh[start_row:end_row , start_col:end_col], 1)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
            cropped_top = cv2.morphologyEx(cropped_top, cv2.MORPH_OPEN, kernel)
            arr = np.array(cropped_top)

            pixel_pctg = arr[np.where(arr >= 1)].size / arr.size * 100
            if (pixel_pctg > 0.01):
                if (pixel_pctg > 0.5 and made == 0):
                    steps = steps + 1
                    made = 1
                elif (pixel_pctg < 0.1 and made == 1):
                    made = 0
                
            # show the output images
            # cv2.imshow("Diff", diff)
            # # cv2.imshow("Thresh", cropped_top)
            plot_data.append((this.frame_count, pixel_pctg))
            this.frame_count = this.frame_count + 1
            #diff = cv2.subtract(gray2, gray1)
            #diff = dilate(erode(diff, 2), 3)
            #diff = morph_dilate(morph_open(diff))
            #print_img(diff)
        return (made, steps)
