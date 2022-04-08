package org.cs_cnu.morsecode;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.pm.PackageManager;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.provider.MediaStore;
import android.util.Log;

import androidx.core.app.ActivityCompat;

import java.nio.ByteBuffer;
import java.util.Map;

public class MorseMicrophoneThread extends Thread {
    public interface MorseMicrophoneCallback {
        void onProgress(String value);
        void onDone(String value);
    }


    final short MORSE_THRESHOLD = Short.MAX_VALUE / 4;
    final float UNSEEN_THRESHOLD = 3.0f;

    final int sample_rate;
    final float frequency;
    final float unit;
    final int unit_size;
    final int buffer_size;

    final MorseMicrophoneThread.MorseMicrophoneCallback callback;

    public MorseMicrophoneThread(MorseMicrophoneThread.MorseMicrophoneCallback callback,
                                 int sample_rate, float frequency, float unit) {
        this.callback = callback;
        this.sample_rate = sample_rate;
        this.frequency = frequency;
        this.unit = unit;
        this.unit_size = (int) Math.ceil(this.sample_rate * this.unit);
        this.buffer_size = (int) AudioRecord.getMinBufferSize(sample_rate, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT);
        setPriority(Thread.MAX_PRIORITY);
    }

    @Override
    public void run() {
        @SuppressLint("MissingPermission")
        final AudioRecord record = new AudioRecord(
                MediaRecorder.AudioSource.DEFAULT,
                this.sample_rate,
                AudioFormat.CHANNEL_IN_MONO,
                AudioFormat.ENCODING_PCM_16BIT,
                2 * sample_rate);

        final short[] samples = new short[unit_size];
        StringBuilder sb = new StringBuilder(); // morse
        int zerocount = 0;
        boolean start = false;

        record.startRecording();
// Need to edit below
        while (true) {
            Log.i("zerocount", String.valueOf(zerocount));
            int result = record.read(samples, 0, unit_size);
            if (result < 0) {
                break;
            }
            for (int i = 0; i < unit_size; i++) { // 데이터가 들어오기 시작할 때 부터 입력하기 위해
                if (samples[i] > MORSE_THRESHOLD) { // samples 배열의 값을 확인
                    start = true;
                    break;
                }
            }
            if(start) {
                int sum = 0;
                double avg = 0;
                for(int i = 0; i < unit_size; i++) {
                    sum += Math.abs(samples[i]);
                }
                avg = sum / unit_size;
                Log.i("avg", String.valueOf(avg));
                if(Math.abs(avg) > 3200){
                    zerocount = 0;
                    sb.append('.');
                }
                else{
                    zerocount += 1;
                    sb.append(' ');
                }
                if(zerocount == 30)
                    break;
            }
            Log.i("result", sb.toString());
        }
        String morse = sb.toString();
        morse = morse.replace("...", "-");
        callback.onDone(morse);
// Need to edit above!
    }
}
