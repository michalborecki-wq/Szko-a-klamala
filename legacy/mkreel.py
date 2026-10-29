import subprocess, sys
def reel(imgs, durs, out, T=0.3):
    inp=[]; 
    for im,d in zip(imgs,durs): inp += ["-loop","1","-t",str(d+T),"-framerate","30","-i",im]
    inp += ["-f","lavfi","-t",str(sum(durs)+T),"-i","anullsrc=r=44100:cl=stereo"]
    f=[]; prev="[0:v]"; off=0
    for i in range(1,len(imgs)):
        off += durs[i-1]
        lab=f"[v{i}]"
        f.append(f"{prev}[{i}:v]xfade=transition={'slideleft' if i%2 else 'fade'}:duration={T}:offset={off:.2f}{lab}")
        prev=lab
    f.append(f"{prev}format=yuv420p,scale=1080:1920[vo]")
    cmd=["ffmpeg","-y",*inp,"-filter_complex",";".join(f),"-map","[vo]","-map",f"{len(imgs)}:a","-c:v","libx264","-r","30","-preset","medium","-crf","20","-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",out]
    subprocess.run(cmd,check=True,capture_output=True)
reel([f"out/p1_historia_reel_0{i}.jpg" for i in range(1,5)],[3.0,4.0,4.0,4.0],"out/p1_historia_reel.mp4")
reel([f"out/p5_chemia_quiz_0{i}.jpg" for i in range(1,8)],[2.2,2.5,1,1,1,4.2,4.0],"out/p5_chemia_quiz.mp4",T=0.2)
