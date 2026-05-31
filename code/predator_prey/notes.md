```
ffmpeg -i new_video.mp4 -filter_complex "[0:v]epx[scaled]" -map "[scaled]" output.mp4
ffmpeg -i output.mp4 -vf "setpts=0.20*PTS" -c:v libx264 -crf 0 -r 120 output_fast.mp4
ffmpeg -i output_fast.mp4 -c:v libx264 -crf 0 -r 60 output_fastq.mp4
ffmpeg -i output_fastq.mp4 -filter_complex "[0:v]crop=x=0:y=0:w=912:h=912[cropped];[cropped]pad=width=912:height=912:x=912:y=0:color=black[padded];[padded]scale=w=1920:h=1080[scaled]" -map "[scaled]" output_end.mp4
ffmpeg -i output_end.mp4 -i norm2.wav -c:v copy -map 0:v -map 1:a -shortest output_sound.mp4
```
