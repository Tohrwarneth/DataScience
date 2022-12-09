package de.hstr.ds.camel;

import org.apache.camel.CamelContext;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.impl.DefaultCamelContext;
import org.apache.camel.model.dataformat.JsonLibrary;
import org.apache.camel.processor.ExchangePatternProcessor;

import java.util.concurrent.atomic.AtomicInteger;

public class CamelExample {
    private static final String PATH = "src/main/resources";
    private static final AtomicInteger state = new AtomicInteger(-1);

    public static void main(String[] args) throws Exception {
        try (CamelContext context = new DefaultCamelContext()) {
            context.addRoutes(new RouteBuilder() {
                @Override
                public void configure() throws Exception {
//                    Aufgabe 1
//
                    from(String.format("stream:file?fileName=%s/measurements.json", PATH)).choice()
                            .when(body().contains("pressure"))
                            .to(String.format("stream:file?fileName=%s/pressure.log", PATH))
                            .otherwise()
                            .to(String.format("stream:file?fileName=%s/temperature.log", PATH));

//                    Aufgabe 2
//
                    from(String.format("stream:file?fileName=%s/measurements2.json", PATH)).choice()
                            //  if
                            .when(body().contains("STOP"))
                            .bean(CamelExample.class, "endState")
                            //  else
                            .otherwise()
                            .unmarshal()
                            .json(JsonLibrary.Jackson, Measurement.class).filter()
                            .ognl("request.body.warning").marshal().json(true)
                            .to("stream:err");
                }
            });
            context.start();
            while (state.get() == -1) {
                Thread.sleep(1000);
            }

            System.out.println();
            context.shutdown();
//            System.exit(state.get());
        }
    }

    public static void endState() {
        state.set(0);
    }
}
