package org.cs_cnu.morsecode;

import android.util.Log;

import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.util.Iterator;
import java.util.Map;

public class MorseSpeakerCodeGenerator implements MorseSpeakerThread.MorseSpeakerIterator {

    final String message;
    final Map<String, String> map;
    final String morse_code;

    public MorseSpeakerCodeGenerator(String message, Map<String, String> map) {
        this.message = message.toUpperCase();
        this.map = map;

// Need to edit below!
        // byte string 생성
        byte[] byteHex = new byte[0];
        byteHex = message.getBytes(StandardCharsets.UTF_8);
        String byteString = new BigInteger(1, byteHex).toString(16).toUpperCase();
        Log.i("hex", byteString);
        // message의 한 문자와 map의 key를 비교하여
        // 같은지 확인
        StringBuilder sb = new StringBuilder();
        for(int i = 0; i < byteString.length(); i++) { // message의 문자들을 반복하며
            for(Map.Entry<String, String> entry : map.entrySet()){ // map의 key들과 비교
                if(String.valueOf(byteString.charAt(i)).equals(entry.getKey())){
                    sb.append(entry.getValue()).append(' ');
                }
            }
            if(String.valueOf(byteString.charAt(i)).equals(" ")){ // 단어사이, / 으로 구분
                sb.append('/');
            }
        }
// Need to edit above!

        this.morse_code = sb.toString();
        Log.i("MorseCode", this.morse_code);
    }

    public String getMorseCode() {
        return this.morse_code;
    }

    @Override
    public int getSize() {
        int size = 0;
        for (int i = 0; i < this.morse_code.length(); i++) {
            char ch = this.morse_code.charAt(i);
            if (ch == '/') {
                size = size + 6; // 단어 사이를 구분하므로
            } else if (ch == ' ') {
                size = size + 1;
            } else if (ch == '.') {
                size = size + 1;
            } else if (ch == '-') {
                size = size + 3;
            }
        }
        size = size + this.morse_code.length();
        return size;
    }

    @Override
    public Iterator<String> iterator() {
        return new Iterator<String> () {
            boolean start = false;
            boolean end = false;
            int i = 0;

            @Override
            public boolean hasNext() {
                if (!start || !end) {
                    return true;
                }
                return false;
            }

            @Override
            public String next() {
                if (!start) {
                    start = true;
                    i = 0;
                }
                if (morse_code.length() > i) {
                    String value = Character.toString(morse_code.charAt(i));
                    i = i + 1;
                    return value;
                } else {
                    end = true;
                }
                return "";
            }
        };
    }
}
