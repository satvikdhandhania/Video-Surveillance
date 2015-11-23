package com.example.android.test.app;

import com.orm.SugarRecord;

/**
 * Created by satvik on 1/5/15.
 */
public class Person extends SugarRecord<Person> {
    String name;
    String time;
    public Person() {

    }

    public Person(String name, String time) {
        this.name = name;
        this.time = time;

    }

}
