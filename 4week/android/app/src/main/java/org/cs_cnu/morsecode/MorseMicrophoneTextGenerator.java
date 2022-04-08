package org.cs_cnu.morsecode;

import android.util.Log;

import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.util.Map;

public class MorseMicrophoneTextGenerator {

    final String morse_code;
    final Map<String, String> map;
    final String text;

    public MorseMicrophoneTextGenerator(String morse_code, Map<String, String> map) {
        this.morse_code = morse_code;
        this.map = map;

// Need to edit below!
        StringBuilder sb = new StringBuilder();
        String[] words = morse_code.split("   "); // 단어로 나눈 배열
        for(int i = 0; i < words.length; i++){
            words[i] = words[i].replace(" ", ""); // 모스 부호 문자간 공백 지우기
            Log.i("word", words[i]);
            for(Map.Entry<String, String> entry: map.entrySet()){
                if(words[i].equals(entry.getValue())) {
                    sb.append(entry.getKey());
                }
            }
            if(words[i].equals("")){ // 단어 사이의 구분
                sb.append(" ");
            }
        }

        byte[] clientByteHex = new byte[sb.length()/2];
        for(int i = 0; i < clientByteHex.length; i++){
            int index = i * 2;
            clientByteHex[i] = (byte) Integer.parseInt(sb.toString().substring(index, index+2), 16);
        }
        String clientOutPut = "";
        try {
            clientOutPut = new String(clientByteHex, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
// Need to edit above!

        this.text = clientOutPut;
        Log.i("Sound input", text);
    }

    public String getText() {
        return this.text;
    }
}
